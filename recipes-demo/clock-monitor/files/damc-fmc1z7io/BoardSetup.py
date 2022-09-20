from HwAccessAarch32 import HwAccessAarch32

CLK_NAMES = {
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

CLK_MON_ADDR = 0x00060000

HW_ACC = HwAccessAarch32
