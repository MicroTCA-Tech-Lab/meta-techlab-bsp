COMPATIBLE_MACHINE = "damc-fmc1z7io|damc-fmc2zup"

DESCRIPTION = "Clock monitor"
LICENSE = "CLOSED"
PV = "2.0"
PR = "r0"

S = "${WORKDIR}"

SRC_URI = " \
    file://clock-monitor.py     \
    file://HwAccessAarch64.py   \
    file://HwAccessAarch32.py   \
    file://BoardSetup.py        \
"

RDEPENDS_${PN} = "python3"

FILES_${PN} = "/opt/mtca-tech-lab/${MACHINE}/clock-monitor/"

do_install() {
    install -d ${D}/opt
    install -d ${D}/opt/mtca-tech-lab/${MACHINE}/clock-monitor/
    cp -r ${WORKDIR}/*.py ${D}/opt/mtca-tech-lab/${MACHINE}/clock-monitor/
}
