echo "fpgautil-init: downloading FPGA image"
fpgautil -b /lib/firmware/base/damc_fmc1z7io_top.bit.bin -o /lib/firmware/base/base.dtbo
echo "fpgautil-init: FPGA image download done"
