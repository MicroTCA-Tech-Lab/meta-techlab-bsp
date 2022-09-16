DESCRIPTION = "FMC1Z7IO demo applications"

inherit packagegroup

Z7IO_DEMO_APPS = "      \
    axi-dma-demo   \
    clock-monitor       \
    irq-handler-demo    \
    io-ctrl-demo        \
"

RDEPENDS_${PN} = "${Z7IO_DEMO_APPS}"
