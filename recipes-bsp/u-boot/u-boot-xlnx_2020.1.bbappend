
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI_append = " \
	file://custom-bootcmd.cfg \
	file://mac-addr.cfg \
	file://0001-Revert-arm64-zynqmp-Remove-all-Xilinx-private-comman.patch \
	file://0002-xilinx-enable-debug-for-MAC-addr-read.patch \
"

