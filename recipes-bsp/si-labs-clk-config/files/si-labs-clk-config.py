#! /usr/bin/env python3

""" Tool for programming Si Labs devices on I2C bus

Example usage:

```
root@damc-fmc2zup:~/silabs# ./si-labs-clk-config.py 0x77 example.txt
INFO:Si5341driver:Device information:
INFO:Si5341driver:  part number: 5341
INFO:Si5341driver:  grade: A
INFO:Si5341driver:  device rev: D
INFO:Si5341driver:  temp grade: Industrial
INFO:Si5341driver:  package id: 9x9 mm 64 QFN
INFO:SiLabsTxtParser:parsing done
INFO:root:programming done
```

"""

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
        description='Program Si Labs device on I2C bus')
    parser.add_argument('--debug', action='store_true',
                        help='print debug information')
    parser.add_argument('--trace', action='store_true',
                        help='print trace information (very verbose)')
    parser.add_argument('--i2c_bus', default=CLK_BUS,
                        help='select I2C bus')
    parser.add_argument('i2c_addr', type=lambda x: int(x, 0),
                        help='address of the device on I2C bus')
    parser.add_argument('--no_reset', action='store_true',
                        help='do not reset the clk gen after the programming')
    parser.add_argument('filename', type=str,
                        help='txt from Si Labs ClockBuilder Pro')

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
    logging.debug("  filename: %s", args.filename)

    clk_bus = smbus.SMBus(args.i2c_bus)
    si5341 = Si534xdriver(clk_bus, args.i2c_addr)
    parser = SiLabsTxtParser(args.filename)
    parser.parse(args.no_reset, si5341.wr)

    logging.log(logging.INFO, "wrote file: %s", args.filename)
    logging.log(logging.INFO, "programming done")


if __name__ == "__main__":
    main()
