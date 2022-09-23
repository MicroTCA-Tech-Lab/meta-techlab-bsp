FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " \
    file://system-user.dtsi \
    file://pl-conf.dtsi \
"

SRC_URI_append_damc-fmc1z7io = " \
    file://0001-Fix-address-size-32-64-bit-for-the-overlay.patch \
"

DEPENDS_append = "${@'device-tree-from-bd' if d.getVar('DT_FROM_BD_ENABLE') == '1' else ''}"

do_configure_append() {
    # append PS config to the main file
    echo '#include "system-user.dtsi"' >> ${DT_FILES_PATH}/system-top.dts

    if [ ${DT_FROM_BD_ENABLE} = "1" ]; then
        # copy the .dts for the app
        cp ${WORKDIR}/recipe-sysroot/opt/mtca-tech-lab/dt/app_from_bd.dts ${DT_FILES_PATH}/board_app.dtsi
    fi

    if [ ${FPGA_MNGR_RECONFIG_ENABLE} = "1" ]; then
        # append PL-related things to the overlay
        echo '/include/ "pl-conf.dtsi"' >> ${DT_FILES_PATH}/pl.dtsi
        if [ ${DT_FROM_BD_ENABLE} = "1" ]; then
            # Create separate PL overlay (.dtbo) for each FPGA variant
            # We create pl_var_<xyz>.dtsi; the upstream recipe will build pl_var_<xyz>.dtbo for us
            for VAR_DTS in ${WORKDIR}/recipe-sysroot/opt/mtca-tech-lab/dt/app_from_bd_*.dts; do
                DTS_BASENAME=$(basename -s .dts ${VAR_DTS})
                FPGA_VARIANT=$(echo ${DTS_BASENAME} | cut -d_ -f4)

                echo "DTS_BASENAME: ${DTS_BASENAME}"
                echo "FPGA_VARIANT: ${FPGA_VARIANT}"

                VAR_DTSI="board_app_${FPGA_VARIANT}.dtsi"
                cp $VAR_DTS ${DT_FILES_PATH}/${VAR_DTSI}
                cp ${DT_FILES_PATH}/pl.dtsi ${DT_FILES_PATH}/pl_var_${FPGA_VARIANT}.dtsi
                echo '/include/ "'${VAR_DTSI}'"' >> ${DT_FILES_PATH}/pl_var_${FPGA_VARIANT}.dtsi
            done
            echo '/include/ "board_app.dtsi"' >> ${DT_FILES_PATH}/pl.dtsi
        fi
    else
        # append PL-related things to the main file
        echo '#include "pl-conf.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
        if [ ${DT_FROM_BD_ENABLE} = "1" ]; then
            echo '#include "board_app.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
        fi
    fi
}
