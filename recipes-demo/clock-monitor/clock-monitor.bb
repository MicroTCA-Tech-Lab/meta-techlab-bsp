COMPATIBLE_MACHINE = "damc-fmc1z7io|damc-fmc2zup"

DESCRIPTION = "Clock monitor"
LICENSE = "CLOSED"
PV = "2.0"
PR = "r0"

FILESEXTRAPATHS_prepend_damc-fmc2zup := "${THISDIR}/files/fmc2zup:"
FILESEXTRAPATHS_prepend_damc-fmc1z7io := "${THISDIR}/files/fmc1z7io:"

S = "${WORKDIR}"

SRC_URI_damc-fmc2zup = "file://clock-monitor.py file://HwAccessAarch64.py"
SRC_URI_damc-fmc1z7io = "file://clock-monitor.py file://HwAccessAarch32.py"

RDEPENDS_${PN} = "python3"

FILES_${PN}_damc-fmc2zup = "/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/"
FILES_${PN}_damc-fmc1z7io = "/opt/mtca-tech-lab/damc-fmc1z7io/clock-monitor/"

do_install_damc-fmc2zup() {
    install -d ${D}/opt
    install -d ${D}/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/
    cp -r ${WORKDIR}/clock-monitor.py ${D}/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/
    cp -r ${WORKDIR}/HwAccessAarch64.py ${D}/opt/mtca-tech-lab/damc-fmc2zup/clock-monitor/
}

do_install_damc-fmc1z7io() {
    install -d ${D}/opt
    install -d ${D}/opt/mtca-tech-lab/damc-fmc1z7io/clock-monitor/
    cp -r ${WORKDIR}/clock-monitor.py ${D}/opt/mtca-tech-lab/damc-fmc1z7io/clock-monitor/
    cp -r ${WORKDIR}/HwAccessAarch32.py ${D}/opt/mtca-tech-lab/damc-fmc1z7io/clock-monitor/
}
