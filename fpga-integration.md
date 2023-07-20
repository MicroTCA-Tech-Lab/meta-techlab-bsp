# Integration of FPGA bitstreams into Yocto system

The handling of FPGA bitstreams and derivation of bin files & device trees is complex and spread across different layers and recipes.

## external-hdf

* `meta-xilinx-tools/recipes-bsp/hdf/external-hdf.bb`
  * Acquires the hardware description `.xsa` declared by `HDF_PATH` in the downstream recipe & installs it to `/opt/xilinx/hw-design/design.xsa`.
  * Deploys the `.xsa` to `${DEPLOYDIR}/Xilinx-${MACHINE}.xsa`.

* `meta-techlab-bsp/recipes-bsp/hdf/external-hdf.bbappend`
  * Acquires and deploys `.xsa` files from `PL_VARIANTS_DIR` when fpga-manager is enabled,
    or falls back to `HDF_PATH`, which must be an absolute path unless the file is provided
    in a further overlay.
  * Filters the `.xsa` files by a regular expression that can be defined as `PL_VARIANTS_FILTER`.
  * Sets a default variant by sorting the XSA file names and taking the highest (last in the list),
    optionally after filtering with another regexp if defined in `PL_VARIANTS_DEFAULT`.
  * Creates text file `/opt/xilinx/hw-design/pl-variants` to list all available variants,
    and `/opt/xilinx/hw-design/pl-variants-default` to show the default variant.

* `meta-<application>/.../hdf/external-hdf.bbappend`
  * Defines `HDF_PATH`, `PL_VARIANTS_DIR`, `PL_VARIANTS_DEFAULT` and provides `.xsa` files.

## device-tree-from-bd

* `meta-techlab-utils/recipes-bsp/device-tree-from-bd/device-tree-from-bd.bb`
  * Iterates through all `.xsa` files provided by `external-hdf` and creates a `app_from_bd_<variant>.dts` for each.

## device-tree

* `meta-techlab-bsp/recipes-bsp/device-tree/device-tree.bbappend`
  * Adds *on-board* (system) peripherals, defined in board-specific `system-user.dtsi`, to `system-top.dts`.
  * Adds *BSP related* information (drivers etc) for PL, defined in board-specific `pl-conf.dtsi`, to `pl.dtsi`.
  * Iterates through `app_from_bd_<variant>.dts` for all variants and for each one, merges it with the other PL related files to `pl-var-<variant>.dtsi`.
  * Upstream `device-tree.bb` will create a `pl-var-<variant>.dtbo` for each of them.

## bitstream-extraction

* `meta-xilinx-tools/recipes-bsp/bitstream/bitstream-extraction_git.bb`
  * Extracts `.bit` file from `.xsa` file.

* `meta-techlab-utils/recipes-bsp/device-tree-from-bd/bitstream-extraction_git.bbappend`
  * Also extracts bitfiles from all variants declared in `/opt/xilinx/hw-design/pl-variants`.

## fpga-manager-util

* `meta-xilinx-tools/recipes-bsp/fpga-manager-util/fpga-manager-util_1.0.bb`
  * Generates binfile from bitfile.
  * Installs binfile & device tree overlay `.dtbo` to `/lib/firmware/...` on rootfs.

* `meta-techlab-utils/recipes-bsp/device-tree-from-bd/fpga-manager-util_%.bbappend`
  * Also creates binfiles and installs binfiles & device tree overlays for each variant.

## fpgautil-init

* `meta-techlab-bsp/recipes-bsp/fpgautil-init/fpgautil-init.bb`
  * Installs init script which downloads the appropriate bitstream into the FPGA & installs the appropriate device tree overlay in the Linux system.
