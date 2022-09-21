COMPATIBLE_MACHINE = "damc-fmc1z7io|damc-fmc2zup"

DESCRIPTION = "IRQ handler demo"
LICENSE = "CLOSED"
PV = "1.0"
PR = "r1"

SRC_URI = "file://irq-handler-demo_v${PV}.tar.gz"
S = "${WORKDIR}/software"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

do_install_append() {
    install -d ${D}${base_prefix}/opt/mtca-tech-lab/${MACHINE}/irq-handler-demo/
    install -m 0755 ${S}/irq_handler_demo  ${D}${base_prefix}/opt/mtca-tech-lab/${MACHINE}/irq-handler-demo/
}

FILES_${PN} = "\
  /opt/mtca-tech-lab/${MACHINE}/irq-handler-demo \
  /opt/mtca-tech-lab/${MACHINE}/irq-handler-demo/irq_handler_demo \
"
