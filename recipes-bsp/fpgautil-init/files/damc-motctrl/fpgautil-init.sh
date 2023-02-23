#!/bin/sh

scriptname="fpgautil-init"

echo "${scriptname}: Downloading FPGA image"
fpgautil -b /lib/firmware/xilinx/base/test/design_1_wrapper.bit.bin -o /lib/firmware/xilinx/base/test/base.dtbo
echo "${scriptname}: FPGA image download done"
