CRIPTION = "Programable Logic reset"
LICENSE = "CLOSED"
LIC_FILES_CHKSUM=""
PV = "1.0.0"
PR = "r0"


FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI_append = " file://fw_plreset.sh"

FILES_${PN} = " \
    /etc/rcS.d/S85fw_plreset \
    /etc/init.d/fw_plreset.sh \
"

do_install_append() {
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d

    install -m 0755 ${WORKDIR}/fw_plreset.sh  ${D}${sysconfdir}/init.d/

    ln -sf ../init.d/fw_plreset.sh  ${D}${sysconfdir}/rcS.d/S85fw_plreset
}

