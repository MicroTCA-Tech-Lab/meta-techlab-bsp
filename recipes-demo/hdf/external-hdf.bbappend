DESCRIPTION = "Recipe to copy externally built HDF to deploy"

LICENSE = "CLOSED"

PROVIDES = "virtual/hdf"

inherit deploy

HDF_BASE = "file://"
HDF_PATH = "damc_fmc2zup_top.xsa"
HDF_NAME = "only-used-for-git"
HDF_EXT = "xsa"

S = "${WORKDIR}"

ZUP_FPGA_VARIANT ?= "zu11eg"


FILESEXTRAPATHS_prepend_damc-fmc2zup := "${THISDIR}/${ZUP_FPGA_VARIANT}:"

