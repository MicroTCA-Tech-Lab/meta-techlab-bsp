DESCRIPTION = "FMC2ZUP-specific support packages"

inherit packagegroup

Z7IO_SUPPORT_PACKAGES = " \
    si-labs-clk-config    \
    fw-plreset            \
    idt-cps-config        \
"

RDEPENDS_${PN} = "${Z7IO_SUPPORT_PACKAGES}"
