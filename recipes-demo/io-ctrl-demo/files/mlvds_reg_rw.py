#! /usr/bin/env python3

# Copyright (c) 2022 Deutsches Elektronen-Synchrotron DESY

import argparse
import logging
import random
import sys
import time

from cpld_interface_lib.MLVDSCtrl import MLVDSCtrl, MLVDSDir, MLVDSRouting


def main():

    LEVEL_DEBUG = logging.DEBUG - 3
    logging.addLevelName(LEVEL_DEBUG, "DEBUG")
    LEVEL_TRACE = logging.DEBUG - 5
    logging.addLevelName(LEVEL_TRACE, "TRACE")

    parser = argparse.ArgumentParser(description="MLVDS Read/Write")

    parser.add_argument(
        "--debug", action="store_true", help="Enable verbose output (debug level)"
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable even more verbose output (trace level)",
    )
    required = parser.add_argument_group("required named arguments")
    parser.add_argument("-w", "--write", help="Set the MLVDS buffer value", default=0x0)
    args = parser.parse_args()

    if args.trace:
        print("Set log level to TRACE")
        logging.basicConfig(level=LEVEL_TRACE)
    elif args.debug:
        print("Set log level to DEBUG")
        logging.basicConfig(level=LEVEL_DEBUG)

    mlvds = MLVDSCtrl()
    mlvds_dir = mlvds.port_dir_get()

    if args.write:
        assert (
            mlvds.cpld_output_routing_get() == MLVDSRouting.REG
        ), "CPLD output routing is not REG. Please run 'mlvds_init' first."
    else:
        assert (
            mlvds.cpld_input_routing_get() == MLVDSRouting.REG
        ), "CPLD input routing is not REG. Please run 'mlvds_init' first."

    if args.write:

        if args.write.startswith("0x"):
            output_val = int(args.write, 16)
        else:
            output_val = int(args.write)

        if mlvds_dir == MLVDSDir.OUT:
            mlvds.port_output_set(output_val)
            print(f"MLVDS output val = {output_val:#04x}")
        elif mlvds_dir == MLVDSDir.IN:
            raise RuntimeError("MLVDS is set to input. Please run 'mlvds_init' first.")
        else:
            raise RuntimeError("Unexpected MLVDS.DIR value")

    else:

        if mlvds_dir == MLVDSDir.IN:
            input_val = mlvds.port_input_get()
            print(f"MLVDS input val = {input_val:#04x}")
        elif mlvds_dir == MLVDSDir.OUT:
            print("MLVDS is set to output. Please run 'mlvds_init' first.")
        else:
            raise RuntimeError("Unexpected MLVDS.DIR value")


if __name__ == "__main__":
    main()
