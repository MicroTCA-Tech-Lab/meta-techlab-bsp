# Copyright (c) 2021 Deutsches Elektronen-Synchrotron DESY

import enum
import logging

from bitstring import BitArray

from cpld_interface_lib.CpldInterface import CpldInterface


class FPIOLevel(enum.Enum):
    LEVEL_3V3 = enum.auto()
    LEVEL_5V = enum.auto()


class FPIODir(enum.Enum):
    OUT = enum.auto()
    IN = enum.auto()


class FPIORouting(enum.Enum):
    REG = enum.auto()
    APP = enum.auto()


class FPIOCtrl:

    """High-level control over the front-panel I/O

    User should first initialize the hardware, and then use the input/output
    methods to set and get the values on the pins. The main methods are:

      * `FPIOCtrl.buf_init`
      * `FPIOCtrl.buf_output_set`
      * `FPIOCtrl.buf_input_get`

    There are a couple of methods which allow changing the configuration of
    the buffers (level, direction, enablement) and can be used to change the
    configuration of an individual 8-bit buffer:

      * `FPIOCtrl.buf_level_set`
      * `FPIOCtrl.buf_dir_set`
      * `FPIOCtrl.buf_enable`

    as well as some methods to retreive the configuration of the buffers:

      * `FPIOCtrl.buf_level_get`
      * `FPIOCtrl.buf_is_enabled`

    There are some methods which provide a way to get and set a single buffer.
    Because ZUP uses 64-bit or 32-bit access this is not so relevent on this
    board, but might be useful on the Z7IO where the interface between the
    FPGA and CPLD is 8 bit wide. Those methods are:

      * `FPIOCtrl.buf_level_set_single`
      * `FPIOCtrl.buf_dir_set_single`
      * `FPIOCtrl.buf_enable_single`

      * `FPIOCtrl.buf_level_get_single`
      * `FPIOCtrl.buf_dir_get_single`
      * `FPIOCtrl.buf_is_enabled_single`

    And there are methods which allow changing the routing of the buffers inside
    the logic. The routing can be switched between CPLD SPI register and Zynq
    application:

      * `FPIOCtrl.cpld_input_routing_set`
      * `FPIOCtrl.cpld_output_routing_set`
      * `FPIOCtrl.cpld_input_routing_get`
      * `FPIOCtrl.cpld_output_routing_get`
    """

    NR_BUFS = 6

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cpld_if = CpldInterface()

    def buf_init(self, dirs, enables, levels=FPIOLevel.LEVEL_3V3):
        """Initialize all buffers

        Args:
            dirs (list of FPIODir): directions
            enables (list of bool): enable buffer
            levels (list of FPIOLevel): voltage level on the front panel I/O
        """
        assert (
            len(dirs) == self.NR_BUFS
        ), f"There are {self.NR_BUFS} buffers to be initialized"

        self.buf_level_set(levels)
        self.buf_dir_set(dirs)
        self.cpld_input_routing_set(FPIORouting.REG)
        self.cpld_output_routing_set(FPIORouting.REG)
        self.buf_enable(enables)

    def buf_init_single(
        self, buf_idx, direct, level=FPIOLevel.LEVEL_3V3, route=FPIORouting.REG
    ):
        """Initialize a single buffer

        Args:
            buf_idx (int): buffer index
            direct (FPIODir): buffer direction
            level (FPIOLevel): voltage level on the front panel I/O
            route (FPIORouting): fpio routing in CPLD
        """
        self.logger.debug("buf_init_single: buf_idx = %d, direct = %s", buf_idx, direct)

        self.buf_level_set_single(buf_idx, level)
        self.buf_dir_set_single(buf_idx, direct)
        if direct == FPIODir.IN:
            self.cpld_input_routing_set(route, buf_idx)
        elif direct == FPIODir.OUT:
            self.cpld_output_routing_set(route, buf_idx)
        else:
            raise RuntimeError("How did we get here?")
        self.buf_enable_single(buf_idx, True)

    def buf_output_set(self, data):
        """Set the entire 48-bit interface

        Args:
            data (int): value to be set (masked with direction)
        """

        self.logger.debug("buf_output_set: data= %#012x", data)
        for i in range(self.NR_BUFS):
            self.cpld_if.output_buffer_set(i, (data >> i * 8) & 0xFF)

    def buf_output_set_single(self, data, buf_idx):
        """Set a single 8-bit buffer

        Note:
            This method is more useful on Z7IO, implemented only for API compatibility

        Args:
            data (int): value to be set (masked with direction)
            buf_idx (int): select a buffer
        """

        assert 0 <= data <= 255, "Only a single buffer"
        assert 0 <= buf_idx < self.NR_BUFS, "Buffer number in limits"

        self.logger.debug(
            "buf_output_set_single: data = %#04x, buf_idx = %d", data, buf_idx
        )

        self.cpld_if.output_buffer_set(buf_idx, data)

    def buf_input_get(self):
        """Read the entire 48-bit interface

        Returns:
            int: current value from the input pins (48-bit)
        """

        data = 0
        for i in range(self.NR_BUFS):
            tmp = self.cpld_if.input_buffer_get(i)
            tmp <<= i * 8
            data |= tmp
        self.logger.debug("buf_input_get: data = %#04x", data)

        return data

    def buf_input_get_single(self, buf_idx=0):
        """Read a single 8-bit buffer

        Note:
            This method is more useful on Z7IO, implemented only for API compatibility

        Args:
            buf_idx (int): buffer index

        Returns:
            int: current value from a single buffer (8-bit)
        """

        assert 0 <= buf_idx < self.NR_BUFS, "Buffer number in limits"

        data_single = self.cpld_if.input_buffer_get(buf_idx)
        self.logger.debug(
            "buf_input_get_single: data = %#04x, buf_idx = %d", data_single, buf_idx
        )

        return data_single

    def buf_level_set(self, levels):
        """Set level for all buffers

        Args:
            level (FPIOLevel): level
        """
        lev_bits = [1 if lev == FPIOLevel.LEVEL_3V3 else 0 for lev in levels]
        lev_val = BitArray(lev_bits[::-1]).uint
        self.cpld_if.lev_set(lev_val)

    def buf_level_set_single(self, buf_idx, level):
        """Set level for a single buffer

        Args:
            buf_idx (int): buffer index
            level (FPIOLevel): level
        """

        assert 0 <= buf_idx < self.NR_BUFS, "Buffer number in limits"
        assert isinstance(
            level, FPIOLevel
        ), "level must be either FPIOLevel.level == FPIOLevel.LEVEL_3V3: or FPIOLevel.LEVEL_5V"

        self.logger.debug(
            "buf_level_set_single: buf_idx = %d, level = %s", buf_idx, level
        )

        lev_vec = self.cpld_if.lev_get()
        if level == FPIOLevel.LEVEL_3V3:
            self.cpld_if.lev_set(lev_vec | (1 << buf_idx))
        elif level == FPIOLevel.LEVEL_5V:
            self.cpld_if.lev_set(lev_vec & ~(1 << buf_idx))
        else:
            raise RuntimeError("How did we get here?")

    def buf_level_get_single(self, buf_idx):
        """Get level for a single buffer

        Args:
            buf_idx (int): buffer index

        Returns:
            FPIOLevel: level
        """
        assert 0 <= buf_idx < self.NR_BUFS, "Buffer number in limits"
        lev_vec = self.cpld_if.lev_get()

        if lev_vec & (1 << buf_idx):
            return FPIOLevel.LEVEL_3V3
        else:
            return FPIOLevel.LEVEL_5V

    def buf_enable(self, ens):
        """Enable all buffers

        When a buffer is not enabled both sides are isolated from each other.

        Args:
            ens (list of bool): enable buffers
        """

        assert len(ens) == self.NR_BUFS, f"There are {self.NR_BUFS} to be initialized"

        self.logger.debug("buf_enable: ens = %s", ens)

        en_bits = [1 if en else 0 for en in ens]
        en_val = BitArray(en_bits[::-1]).uint
        self.cpld_if.output_en_set(en_val ^ 0x3F)  # inverted

    def buf_enable_single(self, buf_idx, en):
        """Enable a single buffer

        When the buffer is not enabled both sides are isolated from each other.

        Args:
            buf_idx (int): buffer index
            en (bool): enable buffer
        """
        assert 0 <= buf_idx < self.NR_BUFS, "Buffer number in limits"

        self.logger.debug("buf_enable_single: buf_idx = %d, en = %s", buf_idx, en)

        oen_vec = self.cpld_if.output_en_get()
        if en:
            self.cpld_if.output_en_set(oen_vec & ~(1 << buf_idx))
        else:
            self.cpld_if.output_en_set(oen_vec | (1 << buf_idx))

    def buf_is_enabled_single(self, buf_idx):
        """Check is a single buffer is enabled

        Returns:
            bool: True if the buffer is enabled
        """
        assert 0 <= buf_idx < self.NR_BUFS, "Buffer number in limits"
        oen_vec = self.cpld_if.output_en_get()
        return not (oen_vec & (1 << buf_idx))

    def buf_dir_set(self, dirs):
        """Set direction for all buffers

        Args:
            dirs (list of FPIODir): direction
        """

        dir_bits = [1 if dir == FPIODir.OUT else 0 for dir in dirs]
        dir_val = BitArray(dir_bits[::-1]).uint
        self.cpld_if.dir_set(dir_val)

    def buf_dir_set_single(self, buf_idx, direct):
        """Set direction for a single buffer

        Args:
            buf_idx (int): buffer index
            direct (FPIODir): direction
        """
        assert 0 <= buf_idx < self.NR_BUFS, "Buffer number in limits"
        assert isinstance(
            direct, FPIODir
        ), "direct must be either FPIODir.OUT or FPIODir.IN"

        self.logger.debug("buf_dir_set_single: buf_idx = %d, dir = %s", buf_idx, direct)

        dir_vec = self.cpld_if.dir_get()
        if direct == FPIODir.OUT:
            self.cpld_if.dir_set(dir_vec | (1 << buf_idx))
        elif direct == FPIODir.IN:
            self.cpld_if.dir_set(dir_vec & ~(1 << buf_idx))
        else:
            raise RuntimeError("How did we get here?")

    def buf_dir_get_single(self, buf_idx):
        """Get the direction for a single buffer

        Args:
            buf_idx (int): buffer index

        Returns:
            FPIODir: direction
        """
        assert 0 <= buf_idx < self.NR_BUFS, "Buffer number in limits"
        dir_vec = self.cpld_if.dir_get()

        if dir_vec & (1 << buf_idx):
            return FPIODir.OUT
        else:
            return FPIODir.IN

    def cpld_input_routing_set(self, routing, buf_idx=0):
        """Set routing for frontpanel buffer 0-5 input

        Args:
            routing (FPIORouting): routing
            buf_idx (int): buffer index
        """
        if routing == FPIORouting.APP:
            rout_val = buf_idx
            assert 0 <= rout_val < self.NR_BUFS, "Buffer number in limits"
        elif routing == FPIORouting.REG:
            rout_val = 0xFF
        else:
            raise RuntimeError("Unexpected routing value")
        self.logger.debug(
            "buf_input_routing_set: buf_idx = %d, routing = %s", buf_idx, routing
        )
        self.cpld_if.buffer_input_routing_set(rout_val)

    def cpld_output_routing_set(self, routing, buf_idx=0):
        """Set routing for frontpanel buffer 0-5 output

        Args:
            routing (FPIORouting): routing
            buf_idx (int): buffer index
        """
        if routing == FPIORouting.APP:
            rout_val = buf_idx
            assert 0 <= rout_val < self.NR_BUFS, "Buffer number in limits"
        elif routing == FPIORouting.REG:
            rout_val = 0xFF
        else:
            raise RuntimeError("Unexpected routing value")
        self.logger.debug(
            "buf_output_routing_set: buf_idx = %d, routing = %s", buf_idx, routing
        )
        self.cpld_if.buffer_output_routing_set(rout_val)

    def cpld_input_routing_get(self):
        """Get routing for frontpanel buffer 0-5 input

        Returns:
            FPIORouting: routing
        """
        rout_val = self.cpld_if.buffer_input_routing_get()
        if rout_val == 0xFF:
            routing = FPIORouting.REG
        elif rout_val >= 0x00 and rout_val <= 0x05:
            routing = FPIORouting.APP
        else:
            raise RuntimeError("Unexpected return value")
        self.logger.debug(
            "buf_input_routing_get: routing = %s, buffer/val = %i", routing, rout_val
        )
        return routing

    def cpld_output_routing_get(self):
        """Get routing for frontpanel buffer 0-5 output

        Returns:
            FPIORouting: routing
        """
        rout_val = self.cpld_if.buffer_output_routing_get()
        if rout_val == 0xFF:
            routing = FPIORouting.REG
        elif rout_val >= 0x00 and rout_val <= 0x05:
            routing = FPIORouting.APP
        else:
            raise RuntimeError("Unexpected return value")
        self.logger.debug(
            "buf_output_routing_get: routing = %s, buffer/val = %i", routing, rout_val
        )
        return routing
