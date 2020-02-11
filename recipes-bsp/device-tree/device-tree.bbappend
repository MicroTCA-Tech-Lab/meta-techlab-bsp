FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "file://system-user.dtsi"

do_configure_append_damc-fmc2zup() {
    echo '#include "system-user.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
}
