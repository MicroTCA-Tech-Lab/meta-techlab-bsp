#! /usr/bin/env python3

import logging
import mmap
import os
import struct

ZYNQMP_AXI_FPD_PL_OFFSET = 0xA0000000
ZYNQMP_AXI_FPD_PL_SIZE = 256 * 1024 * 1024


class HwAccessAarch64:
    def __init__(
        self, mem_offset=ZYNQMP_AXI_FPD_PL_OFFSET, mem_size=ZYNQMP_AXI_FPD_PL_SIZE
    ):
        self.logger = logging.getLogger(self.__class__.__name__)

        user_filename = "/dev/mem"
        self.mem_offset = mem_offset
        self.mem_size = mem_size
        self.fd_user = os.open(user_filename, os.O_RDWR)
        self.mem = mmap.mmap(self.fd_user, self.mem_size,
                             offset=self.mem_offset)
        self.logger.debug("Opened %s, fd = %d", user_filename, self.fd_user)

    def __close__(self):
        self.mem.close()
        os.close(self.fd_user)

    def rd32(self, addr):
        self.logger.debug("read: addr = %#010x ...", addr)
        addr -= self.mem_offset
        bs = self.mem[addr: addr + 4]
        data = struct.unpack("I", bs)[0]
        self.logger.debug("read: ... data = %#010x", data)
        return data

    def wr32(self, addr, data):
        self.logger.debug("write: addr = %#010x, data = %#010X", addr, data)
        addr -= self.mem_offset
        bs = struct.pack("I", int(data))
        self.mem[addr: addr + 4] = bs
