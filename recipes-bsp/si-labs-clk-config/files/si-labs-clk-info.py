#! /usr/bin/env python3

import argparse
import logging

import smbus

from slcc.Si534xdriver import Si534xdriver
from slcc.SiLabsTxtParser import SiLabsTxtParser
from slcc.extra_logging import LEVEL_TRACE

from slcc.BoardConfig import CLK_BUS


def main():
    """ Process input args, parse text file, program the device over I2C """

    parser = argparse.ArgumentParser(
        description='Get info about Si Labs device on I2C bus')
    parser.add_argument('--debug', action='store_true',
                        help='print debug information')
    parser.add_argument('--trace', action='store_true',
                        help='print trace information (very verbose)')
    parser.add_argument('--i2c_bus', default=CLK_BUS,
                        help='select I2C bus')
    parser.add_argument('i2c_addr', type=lambda x: int(x, 0),
                        help='address of the device on I2C bus')
    parser.add_argument('--get_rev', action='store_true',
                        help='print chip revision')

    args = parser.parse_args()

    if args.trace:
        logging.basicConfig(level=LEVEL_TRACE)
        logging.log(LEVEL_TRACE, "logging: enabled TRACE level")
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.log(logging.DEBUG, "logging: enabled DEBUG level")
    else:
        # for get_rev command, be quiet if log level is not given explicitly
        logging.basicConfig(
            level=logging.WARNING if args.get_rev else logging.INFO)

    logging.debug("arguments:")
    logging.debug("  i2c bus: %d", args.i2c_bus)
    logging.debug("  i2c addr: 0x%02x", args.i2c_addr)

    clk_bus = smbus.SMBus(args.i2c_bus)
    si5341 = Si534xdriver(clk_bus, args.i2c_addr)

    if args.get_rev:
        print(si5341.get_rev())


if __name__ == "__main__":
    main()
