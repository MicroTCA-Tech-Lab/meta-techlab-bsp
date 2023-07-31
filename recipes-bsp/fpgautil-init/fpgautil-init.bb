DESCRIPTION = "Program FPGA as a part of the boot process"
LICENSE = "CLOSED"
PV = "1.0"
PR = "r0"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI = " file://fpgautil-init.sh "

FILES_${PN}_append = " \
    ${sysconfdir}/init.d/fpgautil-init.sh \
    ${sysconfdir}/rcS.d/S50fpgautil-init \
"

do_install() {
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d
    install -m 0755 ${WORKDIR}/fpgautil-init.sh  ${D}${sysconfdir}/init.d/
    ln -sf ../init.d/fpgautil-init.sh  ${D}${sysconfdir}/rcS.d/S50fpgautil-init
}

# FIXME: Depend on FPGA manager & devicetree; choose right FPGA variant at runtime

PL_PKG_SUFFIX ?= ""
PKG_${PN} = "${PN}${PL_PKG_SUFFIX}"
PKG_${PN}-lic = "${PN}${PL_PKG_SUFFIX}-lic"
PACKAGES = "${PN}"
