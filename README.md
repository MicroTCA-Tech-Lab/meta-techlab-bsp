# Yocto BSP layer for DAMC-FMC2ZUP and DAMC-FMC1Z7IO

To be used together with [Xilinx Yocto distribution](https://github.com/Xilinx/yocto-manifests)

This layer also requires the `meta-techlab-utils` layer.

## Configuration

### Device tree from block diagram

An xsct script from [`meta-xilinx-tools`](https://github.com/Xilinx/meta-xilinx-tools) generates device tree
entries for all components connected to the Zynq IP block in the Block Diagram.
In an application layer (e.g. `meta-techlab-demo`) that provides an `.xsa` file via `external-hdf.bbappend` those are the IPs
contained in the `system_bsp_...` block design.

Additionally, to provide device tree entries also from the `system_app`
block design, there is a recipe in the `meta-techlab-utils` layer,
which can be activated with the following option in the `conf/local.conf`:

```
DT_FROM_BD_ENABLE = "1"
```

The output of this recipe is `app_from_bd.dts` which gets included by [device-tree.bbappend](recipes-bsp/device-tree/device-tree.bbappend)

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
