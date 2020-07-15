#! /usr/bin/env python3

import sys
import time

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
}

ZUP_EXAMPLE_CLK_NAMES_LEN = max(map(len, ZUP_EXAMPLE_CLK_NAMES.values()))

class ClockMonitor:

    ADDR_ID_REG = 0x0
    ADDR_VERSION = 0x4
    ADDR_CLK_FREQS = 0x10
    CLK_FREQ_NR = 11

    def __init__(self, hw, offs):
        self.hw = hw
        self.offs = offs

    def get_id(self):
        id_reg = self.hw.rd32(self.offs + self.ADDR_ID_REG)
        version = self.hw.rd32(self.offs + self.ADDR_VERSION)
        return id_reg, version

    def print_clocks(self):
        for i in range(self.CLK_FREQ_NR):
            clk_freq_hz = self.hw.rd32(self.offs + self.ADDR_CLK_FREQS + 4*i)
            clk_freq_mhz = clk_freq_hz / 1e6
            print("Clock {{0:2}} ({{1:{sl}}}) = {{2:7.2f}} MHz".format(sl=ZUP_EXAMPLE_CLK_NAMES_LEN).format(i, ZUP_EXAMPLE_CLK_NAMES[i], clk_freq_mhz))

def main():
    hw = HwAccessAarch64()

    if len(sys.argv) != 2:
        print("Usage: {0} ADDR_OFFSET".format(sys.argv[0]))
        return False

    offset = int(sys.argv[1], 0)
    print("offset: 0x{0:x}".format(offset))
    cm = ClockMonitor(hw, offset)
    id_reg, version = cm.get_id()
    print("ID: {0:08x}".format(id_reg))
    print("Version: {0:08x}".format(version))

    cm.print_clocks()

if __name__ == "__main__":
    main()


