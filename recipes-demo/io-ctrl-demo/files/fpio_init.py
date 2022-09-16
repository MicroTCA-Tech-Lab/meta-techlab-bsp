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

    parser = argparse.ArgumentParser(description="Frontpanel IO Initialization")

    parser.add_argument(
        "--debug", action="store_true", help="Enable verbose output (debug level)"
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable even more verbose output (trace level)",
    )
    parser.add_argument(
        "--disable", action="store_true", help="Disable frontpanel IO buffer"
    )
    parser.add_argument(
        "-b", "--buf", help="Number of the frontpanel IO buffer", type=int
    )
    parser.add_argument(
        "-d",
        "--dir",
        choices=["in", "out"],
        help="Set the frontpanel IO buffer direction",
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="CPLD register or application forward",
        default="reg",
        choices=["reg", "app"],
    )
    args = parser.parse_args()

    if args.trace:
        print("Set log level to TRACE")
        logging.basicConfig(level=LEVEL_TRACE)
    elif args.debug:
        print("Set log level to DEBUG")
        logging.basicConfig(level=LEVEL_DEBUG)

    fpio = FPIOCtrl()

    if args.disable:
        print("Disabling buffers ...")
        fpio.buf_init([FPIODir.IN] * 6, [False] * 6, [FPIOLevel.LEVEL_3V3] * 6)
        print("All buffers disabled, exiting...")
        return

    if args.mode == "reg":
        route = FPIORouting.REG
    elif args.mode == "app":
        route = FPIORouting.APP
    else:
        raise RuntimeError("--mode should be given as 'reg' our 'app'")

    if args.dir == "in":
        fpio.buf_init_single(args.buf, FPIODir.IN, FPIOLevel.LEVEL_3V3, route)
    elif args.dir == "out":
        print("This command will enable the outputs on the choosen buffer!")
        print(
            "PLEASE ENSURE THAT THERE IS NO INPUT SIGNAL CONNECTED TO THESE\n"
            "BUFFER IO LINES! OTHERWISE THIS OPERATION MIGHT RESULT IN DAMAGE\n"
            "OF THE DAMC-FMC1Z7IO OR THE CONNECTED EQUIPMENT."
        )
        cont_yn = input("Continue? [yN] ")

        if len(cont_yn) == 0 or not cont_yn[0].lower() == "y":
            return

        # reset buffer reg to 0
        if route == FPIORouting.REG:
            fpio.buf_output_set_single(0x00, args.buf)

        fpio.buf_init_single(args.buf, FPIODir.OUT, FPIOLevel.LEVEL_3V3, route)
    else:
        raise RuntimeError("--dir should be given as 'in' our 'out'")


if __name__ == "__main__":
    main()
