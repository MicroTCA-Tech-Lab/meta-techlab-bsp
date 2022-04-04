DESCRIPTION = "FMC2ZUP demo applications"

inherit packagegroup

Z7IO_DEMO_APPS = "      \
    zup-axi-dma-demo   \
    clock-monitor       \
    irq-handler-demo    \
"

RDEPENDS_${PN} = "${Z7IO_DEMO_APPS}"
