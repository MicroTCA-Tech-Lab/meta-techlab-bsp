# Copyright (c) 2021 Deutsches Elektronen-Synchrotron DESY

import enum
import logging

from cpld_interface_lib.CpldSpiDriver import CpldSpiDriver


class CpldInterface:
    @enum.unique
    class Addrs(enum.IntEnum):
        REG_FW_ID = 0x00
        REG_FW_VER = 0x01
        REG_SCRATCH = 0x02
        REG_BUFFER_SEL_IN = 0x03
        REG_BUFFER_SEL_OUT = 0x04
        REG_BUFFER_DIR = 0x05
        REG_OUTPUT_EN = 0x06
        REG_BUFFER_LEV = 0x07
        REG_MLVDS_BUFFER_DE = 0x08
        REG_BUFFER_OUTPUT_BASE = 0x0A
        REG_BUFFER_INPUT_BASE = 0x10
        REG_MLVDS_DATA_IN = 0x20
        REG_MLVDS_DATA_OUT = 0x21

    REG_ID_EXPECT = 0xC9
    REG_VER_EXPECT = 0x12

    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)
        self.cpld = CpldSpiDriver()
        self._check_id()

    def _log_name(self):
        return "CpldInterface"

    def _check_id(self):
        id_reg = self.cpld.rd(self.Addrs.REG_FW_ID)
        self.logger.debug("CPLD Firmware ID reg = %#x", id_reg)
        version = self.cpld.rd(self.Addrs.REG_FW_VER)
        self.logger.debug("CPLD Firmware VER reg = %#x", version)

        assert id_reg == self.REG_ID_EXPECT, "CPLD identification register mismatch"
        assert version == self.REG_VER_EXPECT, "CPLD version register mismatch"

    def dir_set(self, direct):
        """1 = output, 0 = input"""
        self.cpld.wr(self.Addrs.REG_BUFFER_DIR, direct)

    def dir_get(self):
        return self.cpld.rd(self.Addrs.REG_BUFFER_DIR)

    def output_en_set(self, out_en_n):
        """Inverted! 0 = enable, 1 = disable"""
        self.cpld.wr(self.Addrs.REG_OUTPUT_EN, out_en_n)

    def output_en_get(self):
        return self.cpld.rd(self.Addrs.REG_OUTPUT_EN)

    def lev_set(self, lev):
        """Level: 0 = 3.3V, 1 = 5V"""
        self.cpld.wr(self.Addrs.REG_BUFFER_LEV, lev)

    def lev_get(self):
        return self.cpld.rd(self.Addrs.REG_BUFFER_LEV)

    def output_buffer_set(self, idx, val):
        self.cpld.wr(self.Addrs.REG_BUFFER_OUTPUT_BASE + idx, val)

    def output_buffer_get(self, idx):
        return self.cpld.rd(self.Addrs.REG_BUFFER_OUTPUT_BASE + idx)

    def input_buffer_get(self, idx):
        return self.cpld.rd(self.Addrs.REG_BUFFER_INPUT_BASE + idx)

    def mlvds_dir_set(self, direct):
        """1 = output, 0 = input"""
        self.cpld.wr(self.Addrs.REG_MLVDS_BUFFER_DE, direct)

    def mlvds_dir_get(self):
        return self.cpld.rd(self.Addrs.REG_MLVDS_BUFFER_DE)

    def mlvds_output_set(self, val):
        self.cpld.wr(self.Addrs.REG_MLVDS_DATA_OUT, val)

    def mlvds_output_get(self):
        return self.cpld.rd(self.Addrs.REG_MLVDS_DATA_OUT)

    def mlvds_input_get(self):
        return self.cpld.rd(self.Addrs.REG_MLVDS_DATA_IN)

    def buffer_input_routing_set(self, routing):
        self.cpld.wr(self.Addrs.REG_BUFFER_SEL_IN, routing)

    def buffer_output_routing_set(self, routing):
        self.cpld.wr(self.Addrs.REG_BUFFER_SEL_OUT, routing)

    def buffer_input_routing_get(self):
        return self.cpld.rd(self.Addrs.REG_BUFFER_SEL_IN)

    def buffer_output_routing_get(self):
        return self.cpld.rd(self.Addrs.REG_BUFFER_SEL_OUT)
