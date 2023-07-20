#!/bin/sh

scriptname="fpgautil-init"

echo "${scriptname}: Downloading FPGA image"
fpgautil -b /lib/firmware/xilinx/base/test/pl-full.bit.bin -o /lib/firmware/xilinx/base/test/base.dtbo
echo "${scriptname}: FPGA image download done"
