
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI_append = " \
	file://usb.cfg \
	file://fpga-debugfs.cfg \
	file://0001-i2c-xiic-use-the-name-from-the-DT-for-the-adapter-na.patch \
"
