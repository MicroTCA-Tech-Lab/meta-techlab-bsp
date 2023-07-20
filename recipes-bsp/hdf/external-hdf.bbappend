# Different PL bitstream variants to be included in the Yocto image can be
# placed into PL_VARIANTS_DIR which must then be specified in the project-
# specific external-hdf.bbapend or in conf/local.conf.

HDF_NAME = "only-used-for-git"
HDF_EXT = "xsa"

do_install() {
    if [ ${FPGA_MNGR_RECONFIG_ENABLE} = "1" ]; then
        # Put design.xsa into subfolders for each variant
        HW_DESIGNS=${D}/opt/xilinx/hw-design
        install -d ${HW_DESIGNS}
        for VARIANT in ${PL_VARIANTS_PATHS}; do
            VARIANT_DIR=${HW_DESIGNS}/$(basename $VARIANT .${HDF_EXT})
            echo installing ${VARIANT} to ${VARIANT_DIR}
            install -d ${VARIANT_DIR}
            install -m 0644 ${WORKDIR}/${VARIANT} ${VARIANT_DIR}/design.xsa
        done
        # Save list of variants for dependents (device-tree, bitstream-extraction)
        echo -n "${PL_VARIANTS}"         > ${HW_DESIGNS}/pl-variants
        echo -n "${PL_VARIANTS_DEFAULT}" > ${HW_DESIGNS}/pl-variants-default
    else
        install -d ${D}/opt/xilinx/hw-design
        install -m 0644 ${WORKDIR}/${HDF_PATH} ${D}/opt/xilinx/hw-design/design.xsa
    fi
}

do_deploy() {
    # One single .xsa has to be deployed for FSBL for some reason
    install -d ${DEPLOYDIR}
    install -m 0644 ${WORKDIR}/${HDF_PATH} ${DEPLOYDIR}/Xilinx-${MACHINE}.${HDF_EXT}
}

python () {
    if d.getVar('FPGA_MNGR_RECONFIG_ENABLE', True) == '1':
        hdflist = []
        hdfpath = []

        from pathlib import Path
        pl_variants_dir = d.getVar('PL_VARIANTS_DIR')
        if pl_variants_dir:
            # Filter the results if the variable is defined.
            pl_variants_filter = d.getVar('PL_VARIANTS_FILTER')
            if pl_variants_filter:
                import re
                p = re.compile(pl_variants_filter)
                is_filter_matched = lambda s: True if p.match(s) else False
            else:
                is_filter_matched = lambda s: True

            print(f"Globbing for XSA files in {pl_variants_dir}:")
            globbed = Path(pl_variants_dir).rglob("*." + d.getVar('HDF_EXT'))
            for hdf in globbed:
                rel_path = hdf.relative_to(pl_variants_dir)
                if is_filter_matched(str(rel_path)):
                    hdflist.append(hdf.stem)
                    hdfpath.append(str(rel_path))
                    print(f"  Using    {str(rel_path)}")
                else:
                    print(f"  Dropping {str(rel_path)}")
        else:
            # as a fallback we still support HDF_PATH without PL_VARIANTS_DIR
            hdf = Path(d.getVar('HDF_PATH'))
            hdflist.append(hdf.stem)
            hdfpath.append(str(hdf))

        d.setVar('PL_VARIANTS', ' '.join(hdflist))
        d.setVar('PL_VARIANTS_PATHS', ' '.join(hdfpath))
        d.setVar('SRC_URI', ' '.join([f" {d.getVar('HDF_BASE')}{i}" for i in hdfpath]))
        if pl_variants_dir:
            # bitbake must be told to search this directory so it can find the
            # files in SRC_URI
            d.setVar('FILESEXTRAPATHS', f"{pl_variants_dir}:{d.getVar('PL_VARIANTS_DIR')}")

        print("Determining the default PL variant:")
        pl_variants_default = d.getVar('PL_VARIANTS_DEFAULT')
        hdfdefault = sorted(hdflist)[-1]
        if pl_variants_dir and pl_variants_default:
            # filter the list of variants for the specified regex
            import re
            p = re.compile(pl_variants_default)
            hdflist_for_default = [x for x in hdflist if p.match(x)]
            if hdflist_for_default:
                print(f"  Filtered variants to select from: {hdflist_for_default}")
                hdfdefault = sorted(hdflist_for_default)[-1]
            else:
                print(f"  The filtered list is empty.")
        d.setVar('PL_VARIANTS_DEFAULT', hdfdefault)

        # do_deploy needs HDF_PATH
        if pl_variants_dir:
            d.setVar('HDF_PATH', [x for x in hdfpath if hdfdefault in x][0])

        print(f"Found these XSA files in {pl_variants_dir} or HDF_PATH:")
        print(f"  PL_VARIANTS_PATHS = {d.getVar('PL_VARIANTS_PATHS')}")
        print(f"  PL_VARIANTS = {d.getVar('PL_VARIANTS')}")
        print(f"  PL_VARIANTS_DEFAULT = {d.getVar('PL_VARIANTS_DEFAULT')}")
        print(f"  SRC_URI = {d.getVar('SRC_URI')}")

        d.setVar('PL_VARIANTS_FILES',
            '/opt/xilinx/hw-design/pl-variants ' +
            '/opt/xilinx/hw-design/pl-variants-default ' +
            ' '.join(
                '/opt/xilinx/hw-design/' + v + '/design.xsa'
                for v in hdflist
            )
        )
    else:
        d.setVar('PL_VARIANTS_FILES', '')
}

FILES_${PN} += "${PL_VARIANT_FILES}"

# Override "do_install[noexec]" from upstream
# TODO: Is this still necessary when dependencies are properly declared?
python __anonymous() {
  d.delVarFlag('do_install', 'noexec')
}
