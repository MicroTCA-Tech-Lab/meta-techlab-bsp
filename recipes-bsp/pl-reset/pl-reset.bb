SUMMARY = "Adds script to reset Programmable Logic"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

# This recipe is currently only supported for MPSOC
COMPATIBLE_MACHINE ?= "^$"
COMPATIBLE_MACHINE_zynqmp = ".*"

S = "${WORKDIR}"
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI = " \
    file://pl-reset.py \
"

RDEPENDS_${PN} = "python3 libgpiod-python"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${S}/pl-reset.py ${D}${bindir}/pl-reset.py
}