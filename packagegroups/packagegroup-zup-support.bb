DESCRIPTION = "FMC2ZUP-specific support packages"

inherit packagegroup

ZUP_SUPPORT_PACKAGES = "  \
    si-labs-clk-config    \
    fw-plreset            \
    idt-cps-config        \
"

RDEPENDS_${PN} = "${ZUP_SUPPORT_PACKAGES}"
