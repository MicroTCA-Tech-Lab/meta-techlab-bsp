
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI_append = " \
	file://custom-bootcmd.cfg \
	file://0001-Revert-arm64-zynqmp-Remove-all-Xilinx-private-comman.patch \
"

