# Copyright (c) 2022 Deutsches Elektronen-Synchrotron DESY

import enum
import logging

from bitstring import BitArray

from cpld_interface_lib.CpldInterface import CpldInterface


class MLVDSDir(enum.Enum):
    OUT = enum.auto()
    IN = enum.auto()


class MLVDSRouting(enum.Enum):
    REG = enum.auto()
    APP = enum.auto()


class MLVDSCtrl:

    """High-level control over the backplane port 17 to 20

    User should first initialize the hardware, and then use the input/output
    methods to set and get the values on the ports. The main methods are:

      * `MLVDSCtrl.port_init`
      * `MLVDSCtrl.port_output_set`
      * `MLVDSCtrl.port_input_get'

    There are methods which allow changing the direction of the ports by accessing
    the MLVDS buffers. This can be also done for a single port:

      * `MLVDSCtrl.port_dir_set`
      * `MLVDSCtrl.port_dir_get`

    And there are methods which allow changing the routing of the ports inside the
    logic. The routing can be switched between CPLD SPI register and Zynq
    application:

      * `MLVDSCtrl.cpld_input_routing_set`
      * `MLVDSCtrl.cpld_output_routing_set`
      * `MLVDSCtrl.cpld_input_routing_get`
      * `MLVDSCtrl.cpld_output_routing_get`

    """

    NR_PORTS = 8

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cpld_if = CpldInterface()

    def port_init(self, direct, route):
        """Initialize backplane ports 17-20

        Args:
            direct (MLVDSDir): direction
            route (MLVDSRouting): routing
        """
        self.port_dir_set(direct)
        if direct == MLVDSDir.IN:
            self.cpld_input_routing_set(route)
        elif direct == MLVDSDir.OUT:
            self.cpld_output_routing_set(route)
        else:
            raise RuntimeError("How did we get here?")

    # ToDo (needs change in CPLD)
    # def port_init_single(self, port_idx, direct, route):
    #     """Initialize single backplane port 17-20

    #     Args:
    #         port_idx (int): port index
    #         direct (MLVDSDir): port direction
    #         route (MLVDSRouting): routing
    #     """
    #     self.logger.debug("port_init_single: port_idx = %d, direct = %s", port_idx, direct)
    #     self.port_dir_set_single(port_idx, direct)
    #     self.port_routing_set_single(port_idyx, route)

    def port_output_set(self, data):
        """Set the entire 8-port MLVDS interface

        Args:
            data (int): value to be set (masked with direction)
        """

        self.logger.debug("port_output_set: data= %#012x", data)
        self.cpld_if.mlvds_output_set(data)

    def port_input_get(self):
        """Read the entire 8-port MLVDS interface

        Returns:
            int: current value from the input ports (8-bit)
        """
        data = self.cpld_if.mlvds_input_get()
        self.logger.debug("port_input_get: data = %#04x", data)

        return data

    def port_dir_set(self, dir):
        """Set direction for backplane ports 17-20

        Args:
            dirs (list of MLVDSDir): direction
        """
        dir_bits = [1 if dir == MLVDSDir.OUT else 0 for _ in range(self.NR_PORTS)]
        dir_val = BitArray(dir_bits[::-1]).uint
        self.cpld_if.mlvds_dir_set(dir_val)

    # # ToDo (needs change in CPLD)
    # def port_dir_set_single(self, port_idx, direct):
    #     """Set direction for a single backplane port

    #     Args:
    #         port_idx (int): port index
    #         direct (MLVDSDir): direction
    #     """
    #     assert 0 <= port_idx < self.NR_PORTS, "Port number in limits"
    #     assert isinstance(
    #         direct, MLVDSDir
    #     ), "direct must be either MLVDSDir.OUT or MLVDSDir.IN"

    #     self.logger.debug("port_dir_set_single: port_idx = %d, dir = %s", port_idx, direct)

    #     dir_vec = self.cpld_if.mlvds_dir_get()
    #     if direct == MLVDSDir.OUT:
    #         self.cpld_if.mlvds_dir_set(dir_vec | (1 << port_idx))
    #     elif direct == MLVDSDir.IN:
    #         self.cpld_if.mlvds_dir_set(dir_vec & ~(1 << port_idx))
    #     else:
    #         raise RuntimeError("How did we get here?")

    def port_dir_get(self):
        """Get the direction of the MLVDS buffers

        Returns:
            MLVDSDir: direction
        """
        dir_vec = self.cpld_if.mlvds_dir_get()

        if dir_vec == 0xFF:
            return MLVDSDir.OUT
        elif dir_vec == 0x00:
            return MLVDSDir.IN
        else:
            raise RuntimeError("Unexpected direction value")

    # # ToDo (needs change in CPLD)
    # def port_dir_get_single(self, port_idx):
    #     """Get the direction for a single backplane port

    #     Args:
    #         port_idx (int): port index

    #     Returns:
    #         MLVDSDir: direction
    #     """
    #     assert 0 <= port_idx < self.NR_PORTS, "Port number in limits"
    #     dir_vec = self.cpld_if.mlvds_dir_get()

    #     if dir_vec & (1 << port_idx):
    #         return MLVDSDir.OUT
    #     else:
    #         return MLVDSDir.IN

    def cpld_input_routing_set(self, routing):
        """Set routing for backplane ports 17-20 input

        Args:
            routing (MLVDSRouting): routing
        """
        if routing == MLVDSRouting.APP:
            rout_val = 0x10
        elif routing == MLVDSRouting.REG:
            rout_val = 0xFF
        else:
            raise RuntimeError("Unexpected routing value")
        self.cpld_if.buffer_input_routing_set(rout_val)

    def cpld_output_routing_set(self, routing):
        """Set routing for backplane ports 17-20 output

        Args:
            routing (MLVDSRouting): routing
        """
        if routing == MLVDSRouting.APP:
            rout_val = 0x10
        elif routing == MLVDSRouting.REG:
            rout_val = 0xFF
        else:
            raise RuntimeError("Unexpected routing value")
        self.cpld_if.buffer_output_routing_set(rout_val)

    def cpld_input_routing_get(self):
        """Get routing for backplane ports 17-20 input

        Returns:
            MLVDSRouting: routing
        """
        rout_val = self.cpld_if.buffer_input_routing_get()
        if rout_val == 0xFF:
            routing = MLVDSRouting.REG
        elif rout_val == 0x10:
            routing = MLVDS_Routing.APP
        else:
            raise RuntimeError("Unexpected return value")
        return routing

    def cpld_output_routing_get(self):
        """Get routing for backplane ports 17-20 output

        Returns:
            MLVDSRouting: routing
        """
        rout_val = self.cpld_if.buffer_output_routing_get()
        if rout_val == 0xFF:
            routing = MLVDSRouting.REG
        elif rout_val == 0x10:
            routing = MLVDS_Routing.APP
        else:
            raise RuntimeError("Unexpected return value")
        return routing
