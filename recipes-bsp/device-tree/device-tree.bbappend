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
        if [ ${DT_FROM_BD_ENABLE} = "1" ]; then
            # Create separate PL overlay (.dtbo) for each PL variant
            # We create pl-var-<xyz>.dtsi; the upstream recipe will build pl-var-<xyz>.dtbo for us
            HW_DESIGNS=${RECIPE_SYSROOT}/opt/xilinx/hw-design
            for PL_VARIANT in $(cat ${HW_DESIGNS}/pl-variants); do
                echo "PL_VARIANT: ${PL_VARIANT}"

                VAR_DTS="${WORKDIR}/recipe-sysroot/opt/mtca-tech-lab/dt/app_from_bd_${PL_VARIANT}.dts"
                VAR_DTSI="board_app_${PL_VARIANT}.dtsi"
                cp ${VAR_DTS} ${DT_FILES_PATH}/${VAR_DTSI}
                cp ${DT_FILES_PATH}/pl.dtsi ${DT_FILES_PATH}/pl-var-${PL_VARIANT}.dtsi
                echo '/include/ "'${VAR_DTSI}'"' >> ${DT_FILES_PATH}/pl-var-${PL_VARIANT}.dtsi
                echo '/include/ "pl-conf.dtsi"'  >> ${DT_FILES_PATH}/pl-var-${PL_VARIANT}.dtsi
            done
            echo '/include/ "board_app.dtsi"' >> ${DT_FILES_PATH}/pl.dtsi
            echo '/include/ "pl-conf.dtsi"'   >> ${DT_FILES_PATH}/pl.dtsi
        fi
    else
        if [ ${DT_FROM_BD_ENABLE} = "1" ]; then
            echo '#include "board_app.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
        fi
        # append PL-related things to the main file
        echo '#include "pl-conf.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
    fi
}

do_deploy_append_damc-fmc1z7io-rev-a() {
    # IMAGE_BOOT_FILES on Z7IO uses damc-fmc1z7io-system.dtb
    ln -sf damc-fmc1z7io-rev-a-system.dtb ${DEPLOYDIR}/damc-fmc1z7io-system.dtb
}
