SUMMARY = "Recipe for build an external adi-axi-hdmi Linux kernel module"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"
PV = "2.0"
PR = "r0"

inherit module

SRC_URI = " \
    file://Makefile \
    file://axi_hdmi_drv.h \
    file://axi_hdmi_drv.c \
    file://axi_hdmi_crtc.c \
    file://axi_hdmi_encoder.c \
    file://COPYING \
"

S = "${WORKDIR}"

# The inherit of module.bbclass will automatically name module packages with
# "kernel-module-" prefix as required by the oe-core build environment.