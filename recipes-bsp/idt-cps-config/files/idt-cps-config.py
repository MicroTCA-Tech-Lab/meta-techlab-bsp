#! /usr/bin/env python3

""" Tool for programming IDT clock Cross-Point Switch

"""

import argparse
import enum
import logging
import os
import fcntl
from collections import namedtuple

from i2c_bus_locator import i2c_bus_locator

from idtcpsconfig.IdtCpsConfig import IdtCpsConfig
from idtcpsconfig.config import config_bytes

def main():

    # on DAMC-FMC2ZUP all clock I2c are on the first bus
    ZUP_CLK_BUS = i2c_bus_locator(compat="cdns", addr=0xFF020000)[0]
    ZUP_CLK_MUX_ADDR = 0x58

    logging.basicConfig(level=logging.DEBUG)

    icc = IdtCpsConfig(ZUP_CLK_BUS, ZUP_CLK_MUX_ADDR)
    icc._write_raw(config_bytes)

    logging.info("After the configuration:")
    icc.print_config()


if __name__ == "__main__":
    main()

