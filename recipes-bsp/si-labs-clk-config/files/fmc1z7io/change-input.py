#! /usr/bin/env python3

""" Tool for programming Si Labs devices on I2C bus

"""

import argparse
import enum
import logging

import smbus

from slcc.Si534xdriver import Si534xdriver
from slcc.extra_logging import LEVEL_TRACE

from i2c_bus_locator import i2c_bus_locator


class InputType(enum.IntEnum):
    IN0 = 0
    XTAL = 3
    # only these two are used on the Z7IO

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @staticmethod
    def argparse(s):
        # skip handling errors here, let argparse do the job
        try:
            return InputType[s]
        except KeyError:
            return s


def main():
    """Process input args, parse text file, program the device over I2C"""

    Z7IO_CLK_BUS = i2c_bus_locator(compat="cdns", addr=0xE0004000)[0]

    parser = argparse.ArgumentParser(description="Switch SiLabs inputs")
    parser.add_argument("--debug", action="store_true", help="print debug information")
    parser.add_argument(
        "--trace", action="store_true", help="print trace information (very verbose)"
    )
    parser.add_argument("--i2c_bus", default=Z7IO_CLK_BUS, help="select I2C bus")
    parser.add_argument(
        "i2c_addr", type=lambda x: int(x, 0), help="address of the device on I2C bus"
    )
    parser.add_argument(
        "input",
        type=InputType.argparse,
        choices=list(InputType),
        help="input for Si5341",
    )

    args = parser.parse_args()

    if args.trace:
        logging.basicConfig(level=LEVEL_TRACE)
        logging.log(LEVEL_TRACE, "logging: enabled TRACE level")
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.log(logging.DEBUG, "logging: enabled DEBUG level")
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug("arguments:")
    logging.debug("  i2c bus: %d", args.i2c_bus)
    logging.debug("  i2c addr: 0x%02x", args.i2c_addr)
    logging.debug("  input: %s", args.input)

    clk_bus = smbus.SMBus(args.i2c_bus)
    si5341 = Si534xdriver(clk_bus, args.i2c_addr)

    val = si5341.rd(Si534xdriver.REG_ADDR_IN_CLK_SEL)
    in_sel = (val >> 1) & 0x3
    print(f"In sel before = {str(InputType(in_sel))} (raw = 0x{val:x})")

    si5341.wr(Si534xdriver.REG_ADDR_IN_CLK_SEL, 1 | (args.input << 1) | 8)

    val = si5341.rd(Si534xdriver.REG_ADDR_IN_CLK_SEL)
    in_sel = (val >> 1) & 0x3
    print(f"In sel after = {str(InputType(in_sel))} (raw = 0x{val:x})")


if __name__ == "__main__":
    main()
