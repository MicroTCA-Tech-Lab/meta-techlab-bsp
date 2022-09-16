DESCRIPTION = "Recipe to copy externally built HDF to deploy"

LICENSE = "CLOSED"

PROVIDES = "virtual/hdf"

inherit deploy

HDF_BASE = "file://"
HDF_PATH_damc-fmc2zup = "damc_fmc2zup_top.xsa"
HDF_PATH_damc-fmc1z7io = "damc_fmc1z7io_top.xsa"
HDF_NAME = "only-used-for-git"
HDF_EXT = "xsa"

S = "${WORKDIR}"

ZUP_FPGA_VARIANT ?= "zu11eg"
Z7IO_FPGA_VARIANT ?= "7z045"

FILESEXTRAPATHS_prepend_damc-fmc2zup := "${THISDIR}/fmc2zup/${ZUP_FPGA_VARIANT}:"
FILESEXTRAPATHS_prepend_damc-fmc1z7io := "${THISDIR}/fmc1z7io/${Z7IO_FPGA_VARIANT}:"
