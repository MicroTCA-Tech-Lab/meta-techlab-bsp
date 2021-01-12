FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " \
	file://system-user.dtsi \
	file://gen_app_amba_dts.tcl \
"

do_configure_append_damc-fmc2zup() {
    # get the xsct files
    XSCT_BIN_DIR=$(which xsct)
    XSCT_DIR=$(dirname $(dirname $XSCT_BIN_DIR))

    # generate .dts for the app
    eval xsct -sdx -nodisp -eval 'source ${WORKDIR}/gen_app_amba_dts.tcl ${XSCT_DIR} ${WORKDIR} ${XSCTH_HDF}'
    cp dts_app/zup_app.dts ${DT_FILES_PATH}/zup_app.dtsi

    # append aux dts files (BSP, app PL) to the main dts
    echo '#include "system-user.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
    echo '#include "zup_app.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
}
