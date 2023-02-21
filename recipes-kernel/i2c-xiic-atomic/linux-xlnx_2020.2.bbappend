# Disable upstream, in-kernel version of this driver to allow our own version to be loaded as module

# TODO: Port to 2021.1

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI_append = " \
	file://disable-upstream-xiic.cfg \
"
