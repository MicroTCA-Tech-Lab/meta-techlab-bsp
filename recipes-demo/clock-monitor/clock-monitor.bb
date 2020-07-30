DESCRIPTION = "Clock monitor"
LICENSE = "CLOSED"
PV = "1.0"
PR = "r1"

SRC_URI = "file://clock-monitor.py file://HwAccessAarch64.py"

RDEPENDS_${PN} = "python3"

FILES_${PN} = "/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

do_install() {
    install -d ${D}/opt
    install -d ${D}/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/
    cp -r ${WORKDIR}/clock-monitor.py ${D}/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/
    cp -r ${WORKDIR}/HwAccessAarch64.py ${D}/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/
}
