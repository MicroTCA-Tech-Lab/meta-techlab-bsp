#! /bin/bash

# Copyright (c) 2021 Deutsches Elektronen-Synchrotron DESY


XSCT=../../../../../build/xsct/Vitis/2020.2/bin/xsct

XSCT_DIR=../../../../../build/xsct/Vitis/2020.2/
WORKDIR=work
HDF_OR_XSA_PATH=../../../recipes-demo/hdf/damc-fmc2zup/damc_fmc2zup_top.xsa


mkdir -p $WORKDIR

if [ ! -d $WORKDIR/git ]; then
	git clone https://github.com/xilinx/device-tree-xlnx.git $WORKDIR/git
fi

$XSCT -sdx -nodisp \
	-eval "set ::argv [list \"$XSCT_DIR\" \"$WORKDIR\" \"$HDF_OR_XSA_PATH\"]; \
		set ::argc [llength $::argv]; \
		source ./gen_app_amba_dts.tcl"

