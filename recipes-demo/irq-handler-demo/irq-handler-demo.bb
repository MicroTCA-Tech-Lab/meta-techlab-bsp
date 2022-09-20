COMPATIBLE_MACHINE = "damc-fmc1z7io|damc-fmc2zup"

DESCRIPTION = "IRQ handler demo"
LICENSE = "CLOSED"
PV = "1.0"
PR = "r1"

SRC_URI = "file://irq-handler-demo_v${PV}.tar.gz"
S = "${WORKDIR}/software"

FILESEXTRAPATHS_prepend_damc-fmc2zup := "${THISDIR}/files/fmc2zup:"
FILESEXTRAPATHS_prepend_damc-fmc1z7io := "${THISDIR}/files/fmc1z7io:"

do_install_append_damc-fmc2zup() {
    install -d ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/irq-handler-demo/
    install -m 0755 ${S}/irq_handler_demo  ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/irq-handler-demo/
}
do_install_append_damc-fmc1z7io() {
    install -d ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/irq-handler-demo/
    install -m 0755 ${S}/irq_handler_demo  ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/irq-handler-demo/
}

FILES_${PN}_damc-fmc2zup = "\
  /opt/mtca-tech-lab/damc-fmc2zup/irq-handler-demo \
  /opt/mtca-tech-lab/damc-fmc2zup/irq-handler-demo/irq_handler_demo \
"
FILES_${PN}_damc-fmc1z7io = "\
  /opt/mtca-tech-lab/damc-fmc1z7io/irq-handler-demo \
  /opt/mtca-tech-lab/damc-fmc1z7io/irq-handler-demo/irq_handler_demo \
"
