from HwAccessAarch32 import HwAccessAarch64

CLK_NAMES = {
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

CLK_MON_ADDR = 0xA0060000

HW_ACC = HwAccessAarch64
