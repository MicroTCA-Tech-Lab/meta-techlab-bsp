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

    parser = argparse.ArgumentParser(description="MLVDS Port Initialization")

    parser.add_argument(
        "--debug", action="store_true", help="Enable verbose output (debug level)"
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable even more verbose output (trace level)",
    )
    parser.add_argument("--disable", action="store_true", help="Disable MLVDS buffer")
    parser.add_argument(
        "-d", "--dir", choices=["in", "out"], help="Set the MLVDS port direction"
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

    mlvds = MLVDSCtrl()

    if args.disable:
        print("Disabling buffers ...")
        mlvds.port_init(MLVDSDir.IN, MLVDSRouting.REG)
        print("All buffers disabled, exiting...")
        return

    if args.mode == "reg":
        route = MLVDSRouting.REG
    elif args.mode == "app":
        route = MLVDSRouting.APP
    else:
        raise RuntimeError("--mode should be given as 'reg' our 'app'")

    if args.dir == "in":
        mlvds.port_init(MLVDSDir.IN, route)
    elif args.dir == "out":
        print("This command will enable the outputs on the MLVDS lines (port 17-20)!")
        print(
            "PLEASE ENSURE THAT THERE IS NO INPUT SIGNAL CONNECTED TO THESE\n"
            "MLVDS IO LINES! OTHERWISE THIS OPERATION MIGHT RESULT IN DAMAGE\n"
            "OF THE DAMC-FMC1Z7IO OR OTHER CARDS IN THE SYSTEM."
        )
        cont_yn = input("Continue? [yN] ")

        if len(cont_yn) == 0 or not cont_yn[0].lower() == "y":
            return

        # reset MLVDS buffer reg to 0
        if route == MLVDSRouting.REG:
            mlvds.port_output_set(0x00)

        for _ in range(10):
            if mlvds.port_input_get() != 0:
                raise RuntimeError(
                    "Traffic on the MLVDS lines detected, unable to activate output"
                )

        mlvds.port_init(MLVDSDir.OUT, route)
    else:
        raise RuntimeError("--dir should be given as 'in' our 'out'")


if __name__ == "__main__":
    main()
