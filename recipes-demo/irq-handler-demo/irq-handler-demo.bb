DESCRIPTION = "AXI DMA demo"
LICENSE = "CLOSED"
PV = "1.0"
PR = "r1"

SRC_URI = "file://irq-handler-demo_v${PV}.tar.gz"
S = "${WORKDIR}/software"

do_install_append() {
    install -d ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/irq-handler-demo/
    install -m 0755 ${S}/irq_handler_demo  ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/irq-handler-demo/
}

FILES_${PN} += "\
  /opt/mtca-tech-lab/damc-fmc2zup/irq-handler-demo \
  /opt/mtca-tech-lab/damc-fmc2zup/irq-handler-demo/irq_handler_demo \
"
