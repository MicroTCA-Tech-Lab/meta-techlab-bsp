DESCRIPTION = "FMC1Z7IO-specific support packages"

inherit packagegroup

Z7IO_SUPPORT_PACKAGES = " \
    si-labs-clk-config    \
    ad-cps-config         \
    cpld-interface-lib    \
    adi-axi-hdmi-mod      \
    adv7511-mod           \
    clk-axi-clkgen-mod    \
"

RDEPENDS_${PN} = "${Z7IO_SUPPORT_PACKAGES}"
