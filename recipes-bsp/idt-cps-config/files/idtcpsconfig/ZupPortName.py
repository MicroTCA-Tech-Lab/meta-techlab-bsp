#! /usr/bin/env python3

import enum


@enum.unique
class ZupPortName(enum.IntEnum):
    FMC1_CLK3_BIDIR = 0
    FMC1_CLK2_BIDIR = 1
    CPS_GC2 = 2
    CPS2MPLL = 3
    CPS_GC1 = 4
    Z3_AMC_TCLK = 5
    Z3_AMC_CLK1 = 6
    Z3_RTM_CLK1 = 7
    TCLKA = 8
    TCLKB = 9
    TCLKC = 10
    TCLKD = 11
    WR_PLL3 = 12
    FMC2_CLK3_BIDIR = 13
    FMC2_CLK2_BIDIR = 14
    MPLL2CPS = 15

