# Integration of FPGA bitstreams into Yocto system

The handling of FPGA bitstreams and derivation of bin files & device trees is complex and spread across different layers and recipes.

There are two use cases - either to use `HDF_PATH` and define a single `.xsa` file to be included in the Yocto image,
or to define `PL_VARIANTS_DIR` and `PL_VARIANTS` and use multiple `.xsa` files to be bundled in the image along with their respective device tree overlays.

## Global variables

These have to be defined at a central place visible to all other recipes; e.g. `local.conf` or the application's `layer.conf`.

* `PL_SUFFIX`: Defines an (optional) suffix for the package names of the programmable logic related packages such as `external-hdf`, `bitstream-extraction` etc.
   This makes it possible to assign a project name to the packages, and to avoid name collisions in a shared package feed.
   Example:
   ```
   PL_PKG_SUFFIX = "-example-design"
   ```
   The PL-related packages will then be named `external-hdf-example-design(..).rpm`, `bitstream-extraction-example-design(..).rpm`, etc.

* `PL_VARIANTS`: Defines a set of basenames of `.xsa` files to be bundled into the root filesystem.
   Example:
   ```
   PL_VARIANTS_damc-fmc2zup = "zu11eg zu19eg"
   ```
   The build system will then use the basename and for each variant try to find a file such as `zu11eg.xsa`, `zu11eg-1.2.3.xsa` or `zu11eg-1.2.3-4-g12345678.xsa`.

## external-hdf

* `meta-xilinx-tools/recipes-bsp/hdf/external-hdf.bb`
  * Acquires the hardware description `.xsa` declared by `HDF_PATH` or `PL_VARIANTS_DEFAULT` in the downstream recipe & installs it to `/opt/xilinx/hw-design/design.xsa`.
  * Deploys the `.xsa` to `${DEPLOYDIR}/Xilinx-${MACHINE}.xsa`.

* `meta-techlab-utils/recipes-bsp/hdf/external-hdf.bbappend`
  * Acquires and deploys `.xsa` files when `PL_VARIANTS_DIR` is set,
    or falls back to `HDF_PATH`, which must be an absolute path unless the file is provided
    in a further overlay.
  * Sets a default variant as defined in `PL_VARIANTS_DEFAULT`. If `PL_VARIANTS_DEFAULT` is not set, it uses the first
    `PL_VARIANT` as default one.
  * Picks up version suffixes in filenames such as `zu11eg-1.2.3.xsa` or `zu11eg-1.2.3-45-g12345678.xsa`.

* `meta-<application>/.../hdf/external-hdf.bbappend`
  * Defines `HDF_PATH` or `PL_VARIANTS_DIR`, `PL_VARIANTS_DEFAULT` and provides `.xsa` files.

## device-tree-from-bd

* `meta-techlab-utils/recipes-bsp/device-tree-from-bd/device-tree-from-bd.bb`
  * Creates a `app_from_bd.dts` for the `.xsa` in `HDF_PATH` or `PL_VARIANTS_DEFAULT`.
  * When `PL_VARIANTS` is set, it also iterates through all `.xsa` files provided by `external-hdf` and creates a `app_from_bd_<variant>.dts` for each.

## device-tree

* `meta-techlab-bsp/recipes-bsp/device-tree/device-tree.bbappend`
  * Adds *on-board* (system) peripherals, defined in board-specific `system-user.dtsi`, to `system-top.dts`.
  * Adds *BSP related* information (drivers etc) for PL, defined in board-specific `pl-conf.dtsi`, to `pl.dtsi`.
  * When `PL_VARIANTS` is set, it iterates through `app_from_bd_<variant>.dts` for all variants and for each one, merges it with the other PL related files to `pl-var-<variant>.dtsi`.
  * Upstream `device-tree.bb` will create a `pl-var-<variant>.dtbo` for each of them.

## bitstream-extraction

* `meta-xilinx-tools/recipes-bsp/bitstream/bitstream-extraction_git.bb`
  * Extracts `.bit` file from `.xsa` file.

* `meta-techlab-utils/recipes-bsp/device-tree-from-bd/bitstream-extraction_git.bbappend`
  * Also extracts bitfiles from all variants declared in `PL_VARIANTS`.

## fpga-manager-util

* `meta-xilinx-tools/recipes-bsp/fpga-manager-util/fpga-manager-util_1.0.bb`
  * Generates binfile from bitfile.
  * Installs binfile & device tree overlay `.dtbo` to `/lib/firmware/...` on rootfs.

* `meta-techlab-utils/recipes-bsp/device-tree-from-bd/fpga-manager-util_%.bbappend`
  * Also creates binfiles and installs binfiles & device tree overlays for all `PL_VARIANTS`.

## fpgautil-init

* `meta-techlab-bsp/recipes-bsp/fpgautil-init/fpgautil-init.bb`
  * Installs init script which downloads the appropriate bitstream into the FPGA & installs the appropriate device tree overlay in the Linux system.
