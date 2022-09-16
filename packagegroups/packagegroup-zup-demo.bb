DESCRIPTION = "FMC2ZUP demo applications"

inherit packagegroup

ZUP_DEMO_APPS = "      \
    zup-axi-dma-demo   \
    clock-monitor       \
    irq-handler-demo    \
"

RDEPENDS_${PN} = "${ZUP_DEMO_APPS}"
