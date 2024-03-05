# exclude bitstream from boot.bin if FPGA Manager is enabled
BIF_PARTITION_ATTR_remove_zynqmp = "${@'bitstream' if d.getVar('FPGA_MNGR_RECONFIG_ENABLE') == '1' else ''}"
BIF_PARTITION_ATTR_zynq = "${@'fsbl u-boot-xlnx' if d.getVar('FPGA_MNGR_RECONFIG_ENABLE') == '1' else 'fsbl bitstream u-boot-xlnx'}"
