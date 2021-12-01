#! /usr/bin/env python3

import argparse
import logging

from HwAccessAarch64 import HwAccessAarch64

ZUP_EXAMPLE_CLK_NAMES = {
    0: "PCIe",
    1: "CPS GC1",
    2: "CPS GC2",
    3: "PS PLL",
    4: "FMC1 CLK0",
    5: "FMC1 CLK1",
    6: "FMC2 CLK0",
    7: "FMC2 CLK1",
    8: "FMC1 REF",
    9: "WR PLL1",
    10: "fixed 100",
    11: "DDR4 clk",
    12: "LLL GT clk",
    13: "FMC1 GBT CLK0",
    14: "FMC1 GBT CLK1",
}

ZUP_EXAMPLE_CLK_NAMES_LEN = max(map(len, ZUP_EXAMPLE_CLK_NAMES.values()))

ZUP_EXAMPLE_CLK_MON_ADDR = 0xA0060000


class ClockMonitor:

    ADDR_ID_REG = 0x0
    ADDR_VERSION = 0x4
    ADDR_CLK_FREQS = 0x10

    ID_REG_EXPECT = 0xC10CC302
    CLK_FREQ_MAX_COUNT = 16
    INVALID_REG = 0xDEADBEEF

    def __init__(self, hw, offs):
        self.hw = hw
        self.offs = offs

        id_reg, _ = self.get_id()
        assert id_reg == self.ID_REG_EXPECT

    def get_id(self):
        id_reg = self.hw.rd32(self.offs + self.ADDR_ID_REG)
        version = self.hw.rd32(self.offs + self.ADDR_VERSION)
        return id_reg, version

    def print_clocks(self):
        for i in range(self.CLK_FREQ_MAX_COUNT):
            clk_freq_hz = self.hw.rd32(self.offs + self.ADDR_CLK_FREQS + 4 * i)
            if clk_freq_hz == self.INVALID_REG:
                break

            clk_freq_mhz = clk_freq_hz / 1e6
            try:
                clk_name = ZUP_EXAMPLE_CLK_NAMES[i]
            except KeyError:
                clk_name = "unknown"

            clk_name = clk_name.ljust(ZUP_EXAMPLE_CLK_NAMES_LEN)
            print(f"Clock {i:2} ( {clk_name} ) = {clk_freq_mhz:7.2f} MHz")


def main():

    parser = argparse.ArgumentParser(description="Show clock frequencies")
    parser.add_argument(
        "--hw_addr",
        default=ZUP_EXAMPLE_CLK_MON_ADDR,
        type=int,
        help="Address of the Clock Monitor IP (from Vivado)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable logging",
    )

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    hw_addr = args.hw_addr
    print(f"Hardware address: {hw_addr:#010x}".format(hw_addr))

    hw = HwAccessAarch64()

    cm = ClockMonitor(hw, hw_addr)
    id_reg, version = cm.get_id()
    print(f"ID: {id_reg:#010x}")
    print(f"Version: {version:#010x}")

    cm.print_clocks()


if __name__ == "__main__":
    main()
