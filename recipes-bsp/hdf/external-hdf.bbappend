# Different PL bitstream variants to be included in the Yocto image can be declared using e.g.
# PL_VARIANTS = "foo bar"

HDF_NAME = "only-used-for-git"
HDF_EXT = "xsa"

do_install() {
    if [ ${FPGA_MNGR_RECONFIG_ENABLE} = "1" ]; then
        # Put design.xsa into subfolders for each variant
        HW_DESIGNS=${D}/opt/xilinx/hw-design
        for VARIANT in ${PL_VARIANTS}; do
            VARIANT_DIR=${HW_DESIGNS}/${VARIANT}
            echo installing ${VARIANT} to ${VARIANT_DIR}
            install -d ${VARIANT_DIR}
            install -m 0644 ${WORKDIR}/${VARIANT}/${HDF_PATH} ${VARIANT_DIR}/design.xsa
        done
        # Save list of variants for dependents (device-tree, bitstream-extraction)
        echo -n "${PL_VARIANTS}" > ${HW_DESIGNS}/pl-variants
    else
        install -d ${D}/opt/xilinx/hw-design
        install -m 0644 ${WORKDIR}/${PL_DEFAULT_VARIANT}/${HDF_PATH} ${D}/opt/xilinx/hw-design/design.xsa
    fi
}

do_deploy() {
    # One single .xsa has to be deployed for FSBL for some reason
    install -d ${DEPLOYDIR}
    install -m 0644 ${WORKDIR}/${PL_DEFAULT_VARIANT}/${HDF_PATH} ${DEPLOYDIR}/Xilinx-${MACHINE}.${HDF_EXT}
}

python () {
    if d.getVar('FPGA_MNGR_RECONFIG_ENABLE', True) == '1':
        d.setVar('PL_VARIANT_FILES',
            '/opt/xilinx/hw-design/pl-variants ' +
            ' '.join(
                '/opt/xilinx/hw-design/' + v + '/design.xsa'
                for v in d.getVar('PL_VARIANTS', True).split(' ')
            )
        )
    else:
        d.setVar('PL_VARIANT_FILES', '')
}

FILES_${PN} += "${PL_VARIANT_FILES}"

# Override "do_install[noexec]" from upstream
# TODO: Is this still necessary when dependencies are properly declared?
python __anonymous() {
  d.delVarFlag('do_install', 'noexec')
}
