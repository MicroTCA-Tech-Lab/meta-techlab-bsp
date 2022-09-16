FILESEXTRAPATHS_prepend_damc-fmc2zup := "${THISDIR}/files/fmc2zup:"

SRC_URI_append = " \
	file://mac-addr.cfg \
	file://env.cfg \
	file://custom_default_env.h \
	file://0001-Revert-arm64-zynqmp-Remove-all-Xilinx-private-comman.patch \
	file://0002-xilinx-enable-debug-for-MAC-addr-read.patch \
	file://0003-Add-custom-default-env-settings.patch \
"

do_configure_append() {
    cp ${B}/../custom_default_env.h ${S}/include
}
