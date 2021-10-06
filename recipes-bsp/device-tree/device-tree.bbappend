FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://system-user.dtsi \
    file://pl-conf.dtsi \
"

DEPENDS_append = "${@'device-tree-from-bd' if d.getVar('DT_FROM_BD_ENABLE') == '1' else ''}"

do_configure_append_damc-fmc2zup() {
    # append PS config to the main file
    echo '#include "system-user.dtsi"' >> ${DT_FILES_PATH}/system-top.dts

    if [ ${DT_FROM_BD_ENABLE} = "1" ]; then
        # copy the .dts for the app
        cp ${WORKDIR}/recipe-sysroot/opt/mtca-tech-lab/dt/app_from_bd.dts ${DT_FILES_PATH}/zup_app.dtsi
    fi

    if [ ${FPGA_MNGR_RECONFIG_ENABLE} = "1" ]; then
        # append PL-related things to the overlay
        echo '/include/ "pl-conf.dtsi"' >> ${DT_FILES_PATH}/pl.dtsi
        if [ ${DT_FROM_BD_ENABLE} = "1" ]; then
            echo '/include/ "zup_app.dtsi"' >> ${DT_FILES_PATH}/pl.dtsi
        fi
    else
        # append PL-related things to the main file
        echo '#include "pl-conf.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
        if [ ${DT_FROM_BD_ENABLE} = "1" ]; then
            echo '#include "zup_app.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
        fi
    fi
}
