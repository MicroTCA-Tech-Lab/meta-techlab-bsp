DESCRIPTION = "IO Demo"
LICENSE = "CLOSED"
PV = "1.0"
PR = "r1"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

S = "${WORKDIR}"

SRC_URI = " \
    file://fpio_init.py \
    file://fpio_reg_rw.py \
    file://mlvds_init.py \
    file://mlvds_reg_rw.py \
"

RDEPENDS_${PN} = "python3"

FILES_${PN} += "/opt/mtca-tech-lab/damc-fmc1z7io/io-ctrl-demo/"

do_install() {
    install -d ${D}/opt
    install -d ${D}/opt/mtca-tech-lab/damc-fmc1z7io/io-ctrl-demo/
    cp -r ${WORKDIR}/fpio_init.py ${D}/opt/mtca-tech-lab/damc-fmc1z7io/io-ctrl-demo/
    cp -r ${WORKDIR}/fpio_reg_rw.py ${D}/opt/mtca-tech-lab/damc-fmc1z7io/io-ctrl-demo/
    cp -r ${WORKDIR}/mlvds_init.py ${D}/opt/mtca-tech-lab/damc-fmc1z7io/io-ctrl-demo/
    cp -r ${WORKDIR}/mlvds_reg_rw.py ${D}/opt/mtca-tech-lab/damc-fmc1z7io/io-ctrl-demo/
}
