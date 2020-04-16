#! /usr/bin/env python3

import argparse
import logging
import math
import struct
import time

import smbus


LEVEL_TRACE = logging.DEBUG-5
logging.addLevelName(LEVEL_TRACE, 'TRACE')


class TPS65987:

    I2C_ADDR = 0x38

    # from Table 1-1 in SLVUBH2B
    REG_ADDR_VID = (0, 4)
    REG_ADDR_DID = (1, 4)
    REG_ADDR_PROTO_VER = (2, 4)
    REG_ADDR_MODE = (3, 4)
    REG_ADDR_TYPE = (4, 4)
    REG_ADDR_CUSTOMER_USE = (6, 8)
    REG_TYPE_C_STATE = (0x69, 4)

    REG_ADDR_CMD0 = 8
    REG_ADDR_DATA0 = 9

    # Thunderbolt(TM) Protocol Version. Required to return 1 per current specification.
    EXPECT_PROTO_VER = 1


    def __init__(self, i2c_bus):
        self.logger = logging.getLogger(__name__)
        self.i2c_bus = i2c_bus

    def _rd_block(self, reg):
        """ Reg is defined as (register address, nr of bytes to read) """

        # we request one byte more because the first byte returned is the "Byte Count"
        bs = self.i2c_bus.read_i2c_block_data(self.I2C_ADDR, reg[0], reg[1]+1)
        if bs[0] != reg[1]:
            print("Warn: number of bytes in register does not match the number of bytes req")
        return bs[1:]

    def get_info(self):
        vid = self._rd_block(self.REG_ADDR_VID)
        did = self._rd_block(self.REG_ADDR_DID)
        proto_ver = self._rd_block(self.REG_ADDR_PROTO_VER)
        mode = self._rd_block(self.REG_ADDR_MODE)
        typ = self._rd_block(self.REG_ADDR_TYPE)
        customer_use = self._rd_block(self.REG_ADDR_CUSTOMER_USE)

        vid = struct.unpack("I", bytes(vid))[0]
        did = struct.unpack("I", bytes(did))[0]
        proto_ver = struct.unpack("I", bytes(proto_ver))[0]
        customer_use = struct.unpack("Q", bytes(customer_use))[0]

        assert proto_ver == self.EXPECT_PROTO_VER

        print("VID      = 0x{0:08x}".format(vid))
        print("DID      = 0x{0:08x}".format(did))
        print("ProtoVer = 0x{0:08x}".format(proto_ver))
        print("Cust Use = 0x{0:016x}".format(customer_use))

    def cmd_data(self, cmd, data_in, len_data_out):
        """ Based on 4.3 Command in SLVAE21A

        Arguments:
            cmd: string, e.g. "FLrr"
            data_in: list
            len_data_out: int

        Returns:
            bytes
        """

        if len(data_in) > 0:
            self.logger.log(LEVEL_TRACE, "  data in = %s", data_in)
            self.i2c_bus.write_i2c_block_data(self.I2C_ADDR, self.REG_ADDR_DATA0,
                                              [len(data_in)] + data_in)

        cmd_arr = [len(cmd)] + [ord(ci) for ci in cmd]
        self.logger.log(LEVEL_TRACE, "  cmd = %s", cmd_arr)
        self.i2c_bus.write_i2c_block_data(self.I2C_ADDR, self.REG_ADDR_CMD0, cmd_arr)

        for _ in range(100):
            cmd_readback = self.i2c_bus.read_i2c_block_data(self.I2C_ADDR, self.REG_ADDR_CMD0, 4+1)
            self.logger.log(LEVEL_TRACE, "  cmd readback = %s", cmd_readback[1:])
            time.sleep(0.01)
            if cmd_readback[1:] == [0, 0, 0, 0]:
                break
        else:
            raise RuntimeError("Command returned error")

        data_out = self.i2c_bus.read_i2c_block_data(self.I2C_ADDR, self.REG_ADDR_DATA0,
                                                    len_data_out+1)
        self.logger.log(LEVEL_TRACE, "  data out = %s", data_out[1:])
        return bytes(data_out[1:])

    def diag(self):
        """ Print some diagnostics registers

        The selection of the registers is a little bit arbitrary, we selected
        what has deemed important during the bring-up of DAMC-FMC2ZUP
        """
        type_c_state = self._rd_block(self.REG_TYPE_C_STATE)
        self.logger.log(LEVEL_TRACE, "  Type C state = %s", type_c_state)

        print("Type C State:")
        print("  CC Pin for PD = 0x{0:02x}".format(type_c_state[0]))
        print("  CC1 Pin State = 0x{0:02x}".format(type_c_state[1]))
        print("  CC2 Pin State = 0x{0:02x}".format(type_c_state[2]))
        print("  Type C Port State = 0x{0:02x}".format(type_c_state[3]))

    def lock(self, unlock_key):
        unlock_key_list = list(struct.pack("I", unlock_key))
        bs = self.cmd_data("LOCK", unlock_key_list, 1)
        ret_code = struct.unpack("B", bytes(bs))[0]
        self.logger.debug("Lock/Unlock Host Interface: return code = %d", ret_code)
        return ret_code == 0

    def flrr(self, reg_num):
        bs = self.cmd_data("FLrr", [reg_num], 4)
        read_reg_addr = struct.unpack("I", bytes(bs))[0]
        return read_reg_addr

    def flrd(self, addr):
        addr_list = list(struct.pack("I", addr))
        bs = self.cmd_data("FLrd", addr_list, 16)
        print(bs)

    def flem(self, addr, nr_sectors):
        """ Returns true if erase was successful """

        addr_list = list(struct.pack("I", addr))
        bs = self.cmd_data("FLem", addr_list + [nr_sectors], 1)
        ret_code = struct.unpack("B", bytes(bs))[0]
        self.logger.debug("Flash Memory Erase: return code = %d", ret_code)
        # from Table 4-34
        return ret_code == 0

    def flwd(self, data):
        bs = self.cmd_data("FLwd", data, 1)
        ret_code = struct.unpack("B", bytes(bs))[0]
        self.logger.debug("Flash Memory Write: return code = %d", ret_code)
        return ret_code == 0

    def flad(self, addr):
        addr_list = list(struct.pack("I", addr))
        bs = self.cmd_data("FLad", addr_list, 1)
        ret_code = struct.unpack("B", bytes(bs))[0]
        self.logger.debug("Flash Memory Wr Addr: return code = %d", ret_code)
        return ret_code == 0


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    parser = argparse.ArgumentParser(
        description='Program TI USB-C PD on DAMC-FMC2ZUP')

    parser.add_argument('--debug', action='store_true',
                        help='print debug information')
    parser.add_argument('--trace', action='store_true',
                        help='print trace information (very verbose)')
    parser.add_argument('--program', type=str, nargs=1,
                        help='program bin file to Flash')
    parser.add_argument('--diag', action='store_true', help='print diag info')
    args = parser.parse_args()

    if args.trace:
        logging.basicConfig(level=LEVEL_TRACE)
        logging.log(LEVEL_TRACE, "logging: enabled TRACE level")
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.log(logging.DEBUG, "logging: enabled DEBUG level")
    else:
        logging.basicConfig(level=logging.INFO)


    print("TI USB-C PD Programmer by MicroTCA Tech Lab at DESY")
    logging.log(LEVEL_TRACE, "logging: arguments = %s", args)

    DAMC_FMC2ZUP_TPS_I2C_BUS = 1
    i2c_bus = smbus.SMBus(DAMC_FMC2ZUP_TPS_I2C_BUS)

    tps = TPS65987(i2c_bus)
    tps.get_info()

    if args.program:
        data = open(args.program[0], "rb").read()
        logging.debug("from %s read %d bytes", args.program[0], len(data))

        tps.lock(0)

        TPS_FLASH_SECTOR_SIZE = 4*1024
        sectors_to_erase = math.ceil(len(data) / TPS_FLASH_SECTOR_SIZE)
        logging.debug("sectors to erase: %d", sectors_to_erase)

        tps.flem(0, sectors_to_erase)
        tps.flad(0)

        CHUNK_SIZE = 16
        PROGRESS_BAR_SIZE = 76

        print("Start programming Flash memory")

        for i, chunk in enumerate(chunks(data, CHUNK_SIZE)):
            tps.flwd(list(chunk))

            # print progress bar
            bar_nr_full = math.floor(PROGRESS_BAR_SIZE*(i+1)/(len(data)/CHUNK_SIZE))
            bar_nr_empty = PROGRESS_BAR_SIZE - bar_nr_full
            bar_end = "\n" if (args.debug or args.trace) else "\b"*(PROGRESS_BAR_SIZE+2)
            print("[" + "="*bar_nr_full + " "*bar_nr_empty + "]", end=bar_end)

        if bar_end != "\n":
            print("")

        print("Done programming")
    elif args.diag:
        tps.diag()

if __name__ == "__main__":
    main()
