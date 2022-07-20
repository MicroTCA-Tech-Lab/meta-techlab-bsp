DESCRIPTION = "Driver for DMMC-STAMP mailbox"
LICENSE = "GPLv2"
PV = "1.0.0"

SRC_URI = "git://github.com/MicroTCA-Tech-Lab/mmc-mailbox-driver.git;protocol=https"
SRCREV = "e67c5a490d484b732fa492ae770d0af0b3c331df"

LIC_FILES_CHKSUM = "file://LICENSE;md5=7a5937f875a881b71ac02f9d0947fa61" 

S = "${WORKDIR}/git"

inherit module

# https://lists.yoctoproject.org/pipermail/meta-intel/2018-September/005546.html
DEPENDS += "xz-native bc-native bison-native"

RDEPENDS_${PN} = "i2c-xiic-atomic"

RPROVIDES_${PN} += "kernel-module-mmc-mailbox-driver"
KERNEL_MODULE_AUTOLOAD += " mmc-mailbox-driver"
KERNEL_MODULE_PROBECONF += " mmc-mailbox-driver"
