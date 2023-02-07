FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " \
    file://${MACHINE}.dtsi \
    file://pl-conf.dtsi \
    file://mailbox.dtsi \
"

SRC_URI_append_damc-fmc1z7io = " \
    file://0001-Fix-address-size-32-64-bit-for-the-overlay.patch \
    file://quad-spi.dtsi \
    file://hdmi.dtsi \
    file://pcie-mem.dtsi \
"

SRC_URI_append_damc-motctrl = " \
    file://ethernet-reordering.dtsi \
"

DEPENDS_append = "${@'device-tree-from-bd' if d.getVar('DT_FROM_BD_ENABLE') == '1' else ''}"

# For Z7IO, also handle the -rev-a variant
YAML_DT_BOARD_FLAGS_damc-fmc1z7io ?= "{BOARD ${MACHINE}}"
YAML_DT_BOARD_FLAGS_damc-fmc2zup  ?= "{BOARD damc-fmc2zup}"
YAML_DT_BOARD_FLAGS_damc-motctrl  ?= "{BOARD damc-motctrl}"

do_configure_prepend() {
    # Inject board DTSI file into DTG tool
    cp ${WORKDIR}/${MACHINE}.dtsi ${WORKDIR}/git/device_tree/data/kernel_dtsi/2020.2/BOARD/
}

do_configure_append() {
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

                # We force the binfile name to 'pl-full.bit.bin' both here and in fpga-manager-util_%.bbappend
                # The variants binfiles may have the same name, b/c they live in different subdirectories
                sed -i "/^\([[:space:]]*\)firmware-name/s/\".*\.bit\.bin\"/\"pl-full.bit.bin\"/" ${DT_FILES_PATH}/pl-var-${PL_VARIANT}.dtsi
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

do_configure_append_damc-motctrl() {
    # To overwrite the defaults, DT aliases for the NICs have to be included at the very last
    echo '#include "ethernet-reordering.dtsi"' >> ${DT_FILES_PATH}/system-top.dts
}

do_deploy_append_damc-fmc1z7io-rev-a() {
    # IMAGE_BOOT_FILES on Z7IO uses damc-fmc1z7io-system.dtb
    ln -sf damc-fmc1z7io-rev-a-system.dtb ${DEPLOYDIR}/damc-fmc1z7io-system.dtb
}
