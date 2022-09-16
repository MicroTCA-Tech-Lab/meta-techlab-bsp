#! /usr/bin/env python3

import argparse
import logging

from HwAccessAarch32 import HwAccessAarch32

Z7IO_EXAMPLE_CLK_NAMES = {
    0:  "PCIe           (pcie_clk)      ",
    1:  "PS PLL CLK0    (arm_clk_100)   ",
    2:  "PS PLL CLK1    (arm_clk_200)   ",
    3:  "OSC 200        (PL_CLK)        ",
    4:  "MAIN PLL CLK1  (CLK_BANK33)    ",
    5:  "MAIN PLL CLK2  (LVDS_CLK)      ",
    6:  "MGT PLL CLK1   (MGTCLK0)       ",
    7:  "RTM PLL CLK1   (CLK_BANK35)    ",
    8:  "FMC GBT CLK0   (FMC2_CLK0_M2C) ",
    9:  "FMC GBT CLK1   (FMC2_CLK1_M2C) ",
    10: "EXT CLK        (Frontpanel)    ",
}

Z7IO_EXAMPLE_CLK_NAMES_LEN = max(map(len, Z7IO_EXAMPLE_CLK_NAMES.values()))
Z7IO_EXAMPLE_CLK_MON_ADDR = 0x00060000

class ClockMonitor:

    ADDR_ID_REG = 0x0
    ADDR_VERSION = 0x4
    ADDR_CLK_FREQS = 0x10

    ID_REG_EXPECT = 0xC10CC302
    CLK_FREQ_NR = len(Z7IO_EXAMPLE_CLK_NAMES)
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
        for i in range(self.CLK_FREQ_NR):
            clk_freq_hz = self.hw.rd32(self.offs + self.ADDR_CLK_FREQS + 4*i)
            if clk_freq_hz == self.INVALID_REG:
                break

            clk_freq_mhz = clk_freq_hz / 1e6
            try:
                clk_name = Z7IO_EXAMPLE_CLK_NAMES[i]
            except KeyError:
                clk_name = "unknown"

            clk_name = clk_name.ljust(Z7IO_EXAMPLE_CLK_NAMES_LEN)
            print(f"Clock {i:2} {clk_name} = {clk_freq_mhz:7.2f} MHz")


def main():

    parser = argparse.ArgumentParser(description="Show clock frequencies")
    parser.add_argument(
        "--hw_addr",
        default=Z7IO_EXAMPLE_CLK_MON_ADDR,
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

    hw = HwAccessAarch32()

    cm = ClockMonitor(hw, hw_addr)
    id_reg, version = cm.get_id()
    print(f"ID: {id_reg:#010x}")
    print(f"Version: {version:#010x}")

    cm.print_clocks()

if __name__ == "__main__":
    main()
