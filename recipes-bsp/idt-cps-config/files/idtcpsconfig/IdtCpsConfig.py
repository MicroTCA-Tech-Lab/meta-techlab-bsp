#! /usr/bin/env python3


import logging
import os
import fcntl

from idtcpsconfig.PortConfig import PortConfig


class IdtCpsConfig:

    IOCTL_I2C_SLAVE = 0x0703  # Change slave address

    def __init__(self, i2c_bus, i2c_addr):
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.debug("opening I2C bus %d", i2c_bus)
            self.i2c_bus = os.open("/dev/i2c-{0}".format(i2c_bus), os.O_RDWR)
            self.logger.debug("opened I2C bus, descriptor = %d", self.i2c_bus)

            rc = fcntl.ioctl(self.i2c_bus, self.IOCTL_I2C_SLAVE, i2c_addr)
            self.logger.debug("setting I2C slave address = %s", "OK" if rc == 0 else "ERROR")

    def __del__(self):
        os.close(self.i2c_bus)

    def _read_raw(self) -> bytes:
        buf = os.read(self.i2c_bus, 16)
        return buf

    def _write_raw(self: bytes, buf) -> None:
        os.write(self.i2c_bus, buf)

    def print_config(self):
        for i, b in enumerate(self._read_raw()):
            self.logger.info("port {0:2}: {1}".format(i, PortConfig.from_byte(b)))

