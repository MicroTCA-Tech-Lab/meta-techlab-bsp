DESCRIPTION = "Xilinx I2C driver with support for master_xfer_atomic"
LICENSE = "GPLv2"
PV = "1.0.0"
PR = "r0"

SRC_URI = "git://github.com/MicroTCA-Tech-Lab/i2c-xiic-atomic.git;protocol=https"
SRCREV = "02ff8df7a1c6e9b26991b4f428ffdee5945a655e"

LIC_FILES_CHKSUM = "file://LICENSE;md5=52769200b2e3d34d7d586182ce4081df"

S = "${WORKDIR}/git"

inherit module

# https://lists.yoctoproject.org/pipermail/meta-intel/2018-September/005546.html
DEPENDS += "xz-native bc-native bison-native"

RPROVIDES_${PN} += "kernel-module-i2c-xiic"
KERNEL_MODULE_AUTOLOAD += " i2c-xiic"
KERNEL_MODULE_PROBECONF += " i2c-xiic"
