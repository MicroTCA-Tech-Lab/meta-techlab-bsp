DESCRIPTION = "MOTCTRL-specific support packages"

inherit packagegroup

MOTCTRL_SUPPORT_PACKAGES = " \
    ad-cps-config         \
"

RDEPENDS_${PN} = "${MOTCTRL_SUPPORT_PACKAGES}"
