DESCRIPTION = "mmc-mailbox driver"
LICENSE = "GPL"
PV = "0.0.1"
LIC_FILES_CHKSUM = "file://LICENSE;md5=afcc69d729fbf1d0a2af28ce44a23991" 

SRC_URI = "\
  file://mmc-mailbox-driver.c \
  file://Makefile \
  file://LICENSE \
"
S = "${WORKDIR}"

inherit module

# https://lists.yoctoproject.org/pipermail/meta-intel/2018-September/005546.html
DEPENDS += "xz-native bc-native bison-native"

RPROVIDES_${PN} += "kernel-module-mmc-mailbox-driver"
KERNEL_MODULE_AUTOLOAD += " mmc-mailbox-driver"
KERNEL_MODULE_PROBECONF += " mmc-mailbox-driver"
