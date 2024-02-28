DESCRIPTION = "UNIZUP-specific support packages"

inherit packagegroup

UNIZUP_SUPPORT_PACKAGES = "  \
    si-labs-clk-config    \
    fw-plreset            \
"

RDEPENDS_${PN} = "${UNIZUP_SUPPORT_PACKAGES}"
