#! /usr/bin/env python3

# Copyright (c) 2022 Deutsches Elektronen-Synchrotron DESY

import argparse
import logging
import random
import sys
import time

from cpld_interface_lib.FPIOCtrl import FPIOCtrl, FPIODir, FPIOLevel, FPIORouting


def main():

    LEVEL_DEBUG = logging.DEBUG - 3
    logging.addLevelName(LEVEL_DEBUG, "DEBUG")
    LEVEL_TRACE = logging.DEBUG - 5
    logging.addLevelName(LEVEL_TRACE, "TRACE")

    parser = argparse.ArgumentParser(description="Frontpanel IO Read/Write")

    parser.add_argument(
        "--debug", action="store_true", help="Enable verbose output (debug level)"
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable even more verbose output (trace level)",
    )
    required = parser.add_argument_group("required named arguments")
    required.add_argument(
        "-b",
        "--buf",
        help="Number of the frontpanel IO buffer",
        required=True,
        type=int,
    )
    parser.add_argument(
        "-w", "--write", help="Set the frontpanel output buffer value", default=0x0
    )
    args = parser.parse_args()

    if args.trace:
        print("Set log level to TRACE")
        logging.basicConfig(level=LEVEL_TRACE)
    elif args.debug:
        print("Set log level to DEBUG")
        logging.basicConfig(level=LEVEL_DEBUG)

    fpio = FPIOCtrl()
    buf_dir = fpio.buf_dir_get_single(args.buf)

    assert fpio.buf_is_enabled_single(
        args.buf
    ), "Buffer is not enabled. Please run 'fpio_init' first."
    if args.write:
        assert (
            fpio.cpld_output_routing_get() == FPIORouting.REG
        ), "CPLD output routing is not REG. Please run 'fpio_init' first."
    else:
        assert (
            fpio.cpld_input_routing_get() == FPIORouting.REG
        ), "CPLD input routing is not REG. Please run 'fpio_init' first."

    if args.write:

        if args.write.startswith("0x"):
            output_val = int(args.write, 16)
        else:
            output_val = int(args.write)

        if buf_dir == FPIODir.OUT:
            fpio.buf_output_set_single(output_val, args.buf)
            print(f"Buffer {args.buf:} output val = {output_val:#04x}")
        elif buf_dir == FPIODir.IN:
            raise RuntimeError("Buffer is set to input. Please run 'fpio_init' first.")
        else:
            raise RuntimeError("Unexpected FPIO.DIR value")

    else:

        if buf_dir == FPIODir.IN:
            input_val = fpio.buf_input_get_single(args.buf)
            print(f"Buffer {args.buf:} input val = {input_val:#04x}")
        elif buf_dir == FPIODir.OUT:
            print("Buffer is set to output. Please run 'fpio_init' first.")
        else:
            raise RuntimeError("Unexpected FPIO.DIR value")


if __name__ == "__main__":
    main()
