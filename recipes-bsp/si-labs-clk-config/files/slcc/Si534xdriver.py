#! /usr/bin/env python3

import logging
import struct
from typing import Tuple

import smbus

from slcc.extra_logging import LEVEL_TRACE


LEVEL_TRACE = logging.DEBUG-5
logging.addLevelName(LEVEL_TRACE, 'TRACE')


class Si534xdriver:
    """ Si5340/1 clock generator configuration over I2C

    Developed for DAMC-FMC2ZUP by MicroTCA Tech Lab, but can be also used on
    other boards with the same chip and Linux I2C subsystem.

    Register map from:
    https://www.silabs.com/documents/public/reference-manuals/Si5341-40-D-RM.pdf
    """

    REG_ADDR_PAGE = 0x01

    REG_ADDR_PN_BASE0 = (0x2, 0)
    REG_ADDR_PN_BASE1 = (0x3, 0)
    REG_ADDR_GRADE = (0x4, 0)
    REG_ADDR_DEVICE_REV = (0x5, 0)
    REG_ADDR_TEMP_GRADE = (0x9, 0)
    REG_ADDR_PKG_ID = (0xa, 0)
    REG_ADDR_IN_CLK_SEL = (0x21, 0)

    EXPECTED_PN_BASE = [0x5340, 0x5341]

    TEMP_GRADE_MAP = {
        0x0: "Industrial"
    }

    PKG_ID_MAP = {
        0x0: "9x9 mm 64 QFN",
        0x1: "7x7 mm 64 QFN"
    }

    def __init__(self, bus: smbus.SMBus, addr: int):
        self.bus = bus
        self.addr = addr
        self.logger = logging.getLogger(__name__)
        self.cur_page = None

        self._check_device()

    def _get_pn(self):
        """ Check that the Si5341 device is supported & return part number"""
        pn0 = self.rd(self.REG_ADDR_PN_BASE0)
        pn1 = self.rd(self.REG_ADDR_PN_BASE1)
        pn_base = struct.unpack("H", struct.pack("BB", pn0, pn1))[0]
        assert pn_base in self.EXPECTED_PN_BASE, \
            "Unrecognized Part Number, expected %04x, got %04x" % \
            (self.EXPECTED_PN_BASE, pn_base)
        return pn_base

    def _check_device(self):
        """ Check if the device is Si5341 - part of the init """

        self.logger.debug("_check_device called")

        pn_base = self._get_pn()
        grade = self.rd(self.REG_ADDR_GRADE)
        device_rev = self.rd(self.REG_ADDR_DEVICE_REV)
        temp_grade = self.rd(self.REG_ADDR_TEMP_GRADE)
        pkg_id = self.rd(self.REG_ADDR_PKG_ID)

        temp_grade_str = self.TEMP_GRADE_MAP[temp_grade]
        pkg_id_str = self.PKG_ID_MAP[pkg_id]

        self.logger.info("Device information:")
        self.logger.info("  part number: %04x", pn_base)
        self.logger.info("  grade: %c", chr(ord("A")+grade))
        self.logger.info("  device rev: %c", chr(ord("A")+device_rev))
        self.logger.info("  temp grade: %s", temp_grade_str)
        self.logger.info("  package id: %s", pkg_id_str)

    def get_rev(self):
        """ Get Si5341 device revision """
        self._get_pn()
        device_rev = self.rd(self.REG_ADDR_DEVICE_REV)
        return chr(ord("A")+device_rev)

    def _set_page(self, page: int):
        self.logger.log(LEVEL_TRACE, "setting page to %d", page)
        self.bus.write_byte_data(self.addr, self.REG_ADDR_PAGE, page)
        self.cur_page = page

    def rd(self, addr: Tuple[int, int]):
        """ Read a single byte, addr in format (reg addr, page addr)"""
        if self.cur_page != addr[1]:
            self._set_page(addr[1])
        self.bus.write_byte(self.addr, addr[0])
        b = self.bus.read_byte(self.addr)
        self.logger.log(
            LEVEL_TRACE, "read: addr = %02x, data = %02x", addr[0], b)
        return b

    def wr(self, addr: Tuple[int, int], val: int):
        """ Write a single byte, addr in format (reg addr, page addr)"""
        if self.cur_page != addr[1]:
            self._set_page(addr[1])
        self.bus.write_byte_data(self.addr, addr[0], val)
        self.logger.log(
            LEVEL_TRACE, "write: addr = %02x, data = %02x", addr[0], val)


def main():
    """ Example usage, reads info from the I2C device """

    Z7IO_CLK_BUS = 0
    Z7IO_SI5341_PL_ADDR = 0x77

    logging.basicConfig(level=logging.DEBUG)

    clk_bus = smbus.SMBus(Z7IO_CLK_BUS)
    si5341 = Si5341driver(clk_bus, Z7IO_SI5341_PL_ADDR)
    si5341._check_device()  # pylint: disable=protected-access


if __name__ == "__main__":
    main()
