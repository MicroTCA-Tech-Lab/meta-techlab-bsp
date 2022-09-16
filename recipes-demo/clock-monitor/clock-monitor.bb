DESCRIPTION = "Clock monitor"
LICENSE = "CLOSED"
PV = "2.0"
PR = "r0"

SRC_URI = "file://clock-monitor.py file://HwAccessAarch64.py"

RDEPENDS_${PN} = "python3"

FILES_${PN} = "/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/"

FILESEXTRAPATHS_prepend_damc-fmc2zup := "${THISDIR}/files/fmc2zup:"

do_install() {
    install -d ${D}/opt
    install -d ${D}/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/
    cp -r ${WORKDIR}/clock-monitor.py ${D}/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/
    cp -r ${WORKDIR}/HwAccessAarch64.py ${D}/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/
}
