
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI_append = " \
	file://usb.cfg \
	file://fpga-debugfs.cfg \
"
