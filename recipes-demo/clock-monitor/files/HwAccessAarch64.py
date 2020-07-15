#! /usr/bin/env python3

import logging
import mmap
import os
import struct
import subprocess

class HwAccessAarch64(object):

  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)

    user_filename = "/dev/mem"
    self.fd_user = os.open(user_filename, os.O_RDWR)
    self.mem = mmap.mmap(self.fd_user, 256 * 1024 * 1024, offset=0x80000000)
    self.logger.debug("Opened %s, fd = %d", user_filename, self.fd_user)


  def __close__(self):
    self.mem.close()
    os.close(self.fd_user)

  def rd32(self, addr):
    addr_w_o = addr
    bs = self.mem[addr_w_o:addr_w_o + 4]
    return struct.unpack("I", bs)[0]

  def wr32(self, addr, data):
    bs = struct.pack("I", int(data))
    addr_w_o = addr
    self.mem[addr_w_o:addr_w_o + 4] = bs

  def rd_bytes(self, addr, length):
    bs = b""
    for i in range(0, length//4):
      addr_w_o = addr + 4*i
      b = self.mem[addr_w_o:addr_w_o + 4]
      bs += b
    return bs[0:length]

def main():
  hw = HwAccessAarch64()
  print("ID reg: {0:08x}".format(hw.rd32(0x0)))
  print("version: {0:08x}".format(hw.rd32(0x4)))

if __name__ == "__main__":
  main()


