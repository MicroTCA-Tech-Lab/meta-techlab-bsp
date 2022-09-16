DESCRIPTION = "Program FPGA as a part of the boot process"
LICENSE = "CLOSED"
PV = "1.0"
PR = "r0"

SRC_URI = " file://fpgautil-init.sh "

FILES_${PN}_append = " \
    /etc/init.d/fpgautil-init.sh \
    /etc/rcS.d/S50fpgautil-init \
"

do_install() {
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d
    install -m 0755 ${WORKDIR}/fpgautil-init.sh  ${D}${sysconfdir}/init.d/
    ln -sf ../init.d/fpgautil-init.sh  ${D}${sysconfdir}/rcS.d/S50fpgautil-init
}

# FIXME: Depend on FPGA manager, hdf & devicetree; choose right FPGA variant at runtime
