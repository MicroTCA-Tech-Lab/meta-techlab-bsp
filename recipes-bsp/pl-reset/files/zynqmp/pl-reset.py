#!/usr/bin/env python3

import argparse
import gpiod

PL_RESET_PIN = 173

def pl_reset(value: int):

    for chip in gpiod.ChipIter():
        if chip.label() == "zynqmp_gpio":
                pl_reset = chip.get_line(PL_RESET_PIN)
                pl_reset.request(consumer="reset_pl", type=gpiod.LINE_REQ_DIR_OUT)

                pl_reset.set_value(value)
                return 0
    
    print("Unable to find GPIO for PL reset!")
    return -1



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Sets PL Reset to the specified value [0 = LOW, 1 = HIGH]')
    
    parser.add_argument('value', type=int, nargs=1, choices=[0,1], help='Reset line value')
    args = parser.parse_args()

    pl_reset(args.value[0])