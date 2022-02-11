# Yocto layer for DAMC-FMC2ZUP

To be used together with Xilinx Yocto distribution, available at:

https://github.com/Xilinx/yocto-manifests

This layer also requires `meta-techlab-utils` layer.

## Configuration

### Device tree from block diagram

An xsct script from `meta-xilinx-tool` layer generates a device tree
entries for all components connected to the Zynq IP block in the Block
Diagram. In DAMC-FMC2ZUP BSP those are the IPs contained in the
`system_bsp_fmc2zup` block design.

Additionally, to provide device tree entires also from the `system_app`
block design, there is a recipe in the `meta-techlab-utils` layer,
which can be activeted with the following option in the `conf/local.conf`:

```
DT_FROM_BD_ENABLE = "1"
```

The output of this recipe is `app_from_bd.dts` which has to be included
by the `device-tree.bbappend` in the application layer. See
[recipes-bsp/device-tree/device-tree.bbappend](recipes-bsp/device-tree/device-tree.bbappend)
for an example.

### FPGA manager

FPGA manager can be enabled in `conf/local.conf` with the following line:

```
IMAGE_FEATURES += " fpga-manager"
```

When enabled, a separate device tree overlay (`.dtbo`) is generated,
and the bitstream (for the Programmable Logic) is provided in the
Linux userspace. In this case the PL is programmed from an init
script from Linux userspace instead of u-boot.

Please check [Xilinx Wiki: Solution Zynq PL Programming With FPGA Manager](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841645/Solution+Zynq+PL+Programming+With+FPGA+Manager)
for more information.

### FPGA variant

To select between the two FPGA variants which can be found on DAMC-FMC2ZUP,
Provided in the demo examples are two .xsa files, and user can chose
between the two variants in `conf/local.conf`.

`ZUP_FPGA_VARIANT` should be set to either `"zu11eg"` or `"zu19eg"`. By
default, `"zu11eg"` is used.

### Device Tree entries for the I2C controllers in the Programmable Logic

On the DAMC-FMC2ZUP there are three I2C buses connected to the Programmable
Logic: White Rabbit bus, DS28C36 bus and front panel bus. To manage those
I2C buses the example design contains three Xilinx IIC controllers:

  * `iic_axi_iic_ds28c36`
  * `iic_axi_iic_fplink`
  * `iic_axi_iic_wr`

If the device tree is generated from the application block diagram (when
the `DT_FROM_BD_ENABLE` option is enabled) the device tree entries for
those controllers are declared to be compatible with `"generic-uio"`.

To make those IIC controllers use the Xilinx IIC driver, an option
called `ZUP_DEVICE_TREE_FOR_PL_I2C` is provided. This option enables
the inclusion of an additional device tree file which overrides the
`compatible` value for the three IIC controllers.

To use this function, add the following line to `conf/local.conf`:

```
ZUP_DEVICE_TREE_FOR_PL_I2C = "1"
```

## Demo

This Yocto layer provides also a small demo, which includes an FPGA
bitstream (in `recipes-demo/hdf` directory). Actuall applications are expected
to override the `.xsa` files in this repository with their own files in
an application layer.
