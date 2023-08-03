SUMMARY = "Recipe for build an external adv7511 Linux kernel module"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"
PV = "2.0"
PR = "r0"

inherit module

SRC_URI = " \
    file://Makefile \
    file://adv7511.h \
    file://adv7511_drv.c \
    file://adv7511_audio.c \
    file://adv7511_cec.c \
    file://adv7511_debugfs.c \
    file://adv7533.c \
    file://COPYING \
"

S = "${WORKDIR}"

# The inherit of module.bbclass will automatically name module packages with
# "kernel-module-" prefix as required by the oe-core build environment.