#! /usr/bin/env python3

import logging
import struct
from typing import Tuple

import smbus

from adn.extra_logging import LEVEL_TRACE


LEVEL_TRACE = logging.DEBUG-5
logging.addLevelName(LEVEL_TRACE, 'TRACE')

class ADN4612driver:
    REG_ADDR_REV_ID = 0xFE
    REG_ADDR_CHIP_ID = 0xFF

    EXPECTED_CHIP_ID = [0x12]

    def __init__(self, bus: smbus.SMBus, addr: int):
        self.bus = bus
        self.addr = addr
        self.logger = logging.getLogger(__name__)
        self.cur_page = None

        self._check_device()

    def _check_device(self):
        """ Check if the device is ADN4612 - part of the init """

        self.logger.debug("_check_device called")

        chip_id = self.rd(self.REG_ADDR_CHIP_ID)
        assert chip_id in self.EXPECTED_CHIP_ID, \
            "Unrecognized Part Number, expected %04x, got %04x" % \
            (self.EXPECTED_CHIP_ID, chip_id)

        revision_id = self.rd(self.REG_ADDR_REV_ID)

        self.logger.info("Device information:")
        self.logger.info("  revision id: 0x%02x", revision_id)
        self.logger.info("  chip id: 0x%02x", chip_id)

    def rd(self, addr: int):
        """ Read a single byte """
        self.bus.write_byte(self.addr, addr)
        b = self.bus.read_byte(self.addr)
        self.logger.log(LEVEL_TRACE, "read: addr = %02x, data = %02x", addr, b)
        return b

    def wr(self, addr: int, val: int):
        """ Write a single byte """
        self.bus.write_byte_data(self.addr, addr, val)
        self.logger.log(LEVEL_TRACE, "write: addr = %02x, data = %02x", addr, val)


def main():
    """ Example usage, reads info from the I2C device """

    Z7IO_CLK_BUS = 0
    Z7IO_ADN4212_PL_ADDR = 0x44

    logging.basicConfig(level=logging.DEBUG)

    clk_bus = smbus.SMBus(Z7IO_CLK_BUS)
    adn4612 = ADN4612driver(clk_bus, Z7IO_ADN4212_PL_ADDR)
    adn4612._check_device()  # pylint: disable=protected-access

if __name__ == "__main__":
    main()
