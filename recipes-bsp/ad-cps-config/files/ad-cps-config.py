#! /usr/bin/env python3

""" Tool for programming ADN4612 devices on I2C bus

Example usage:

```
root@damc-fmc2zup:~/silabs# ./adn-cps-config.py 0x44 example.txt
INFO:ADN4612driver:Device information:
INFO:ADN4612driver:  revision id: 0x00
INFO:ADN4612driver:  chip id: 0x12
INFO:ADN4612TxtParser:parsing done
INFO:root:programming done
```

"""

import argparse
import logging

import smbus

from adn.ADN4612driver import ADN4612driver
from adn.ADN4612TxtParser import ADN4612TxtParser
from adn.extra_logging import LEVEL_TRACE

from adn.DefaultI2c import DEFAULT_I2C_BUS


def main():
    """ Process input args, parse text file, program the device over I2C """

    parser = argparse.ArgumentParser(
        description='Program AD4612 device on I2C bus')
    parser.add_argument('--debug', action='store_true',
                        help='print debug information')
    parser.add_argument('--trace', action='store_true',
                        help='print trace information (very verbose)')
    parser.add_argument('--i2c_bus', default=DEFAULT_I2C_BUS,
                        help='select I2C bus')
    parser.add_argument('i2c_addr', type=lambda x: int(x, 0),
                        help='address of the device on I2C bus')
    parser.add_argument('filename', type=str,
                        help='txt file for ADN4612 register configuration')

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
    adn4674 = ADN4612driver(clk_bus, args.i2c_addr)
    parser = ADN4612TxtParser(args.filename)
    parser.parse(adn4674.wr)

    logging.log(logging.INFO, "wrote file: %s", args.filename)
    logging.log(logging.INFO, "programming done")


if __name__ == "__main__":
    main()
