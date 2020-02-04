DESCRIPTION = "Recipe to copy externally built HDF to deploy"

LICENSE = "CLOSED"

PROVIDES = "virtual/hdf"

inherit deploy

#HDF_BASE ?= "git://"
#HDF_PATH ?= "github.com/xilinx/hdf-examples.git"
#HDF_NAME ?= "system.hdf"

#Set HDF_EXT to "dsa" if you want to use a dsa file instead of hdf.
#HDF_EXT ?= "hdf"

SRC_URI = "file://system_wrapper.hdf"

S = "${WORKDIR}"

FILESEXTRAPATHS_prepend_damc-fmc2zup := "${THISDIR}:"

do_deploy() {
    install -d ${DEPLOYDIR}
    bbnote "Workdir: ${WORKDIR}"
    install -m 0644 ${WORKDIR}/system_wrapper.hdf ${DEPLOYDIR}/Xilinx-${MACHINE}.${HDF_EXT}
}
