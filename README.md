# Yocto BSP layer for DAMC-FMC2ZUP and DAMC-FMC1Z7IO

To be used together with [Xilinx Yocto distribution](https://github.com/Xilinx/yocto-manifests)

This layer also requires the `meta-techlab-utils` layer.

## Configuration

### Device tree from block diagram

An xsct script from [`meta-xilinx-tools`](https://github.com/Xilinx/meta-xilinx-tools) layer generates device tree
entries for all components connected to the Zynq IP block in the Block
Diagram. In DAMC-FMC2ZUP/-FMC1Z7IO BSP those are the IPs contained in the
`system_bsp_fmc2zup`/`_fmc1z7io` block design.

Additionally, to provide device tree entries also from the `system_app`
block design, there is a recipe in the `meta-techlab-utils` layer,
which can be activated with the following option in the `conf/local.conf`:

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

## FPGA bitstream integration

See [fpga-integration.md](fpga-integration.md) for a detailed view of how FPGA bitstreams are handled in the Yocto system.
