FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "      \
    file://issue  \
    file://banner \
"

do_install_basefilesissue_custom () {
	install -m 644 ${WORKDIR}/issue*  ${D}${sysconfdir}
	install -m 644 ${WORKDIR}/banner  ${D}${sysconfdir}
}

BASEFILESISSUEINSTALL = "do_install_basefilesissue_custom"
