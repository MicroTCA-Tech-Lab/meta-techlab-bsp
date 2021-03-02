# Yocto layer for DAMC-FMC2ZUP

To be used together with Xilinx Yocto distribution, available at:

https://github.com/Xilinx/yocto-manifests


## Demo

This Yocto layer provides also a small demo, which includes an FPGA
bitstream (in `recipes-demo/hdf` directory). Actuall applications are expected
to override the `.xsa` files in this repository with their own files.

To select between the two FPGA variants which can be found on DAMC-FMC2ZUP,
`ZUP_FPGA_VARIANT` should be set to either `"zu11eg"` or `"zu19eg"`. By
default, `"zu11eg"` is used.

