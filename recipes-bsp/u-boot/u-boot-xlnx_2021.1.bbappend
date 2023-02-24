FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " \
	file://0001-xilinx-enable-debug-for-MAC-addr-read.patch \
	file://custom_default_env.h \
	file://mac-addr.cfg \
	file://env.cfg \
"

SRC_URI_append_zynq = " \
	file://0001-zynq-Add-custom-default-env-settings.patch \
	file://0002-zynq-Use-fixed-env-location-depending-on-build-time-.patch \
"

SRC_URI_append_zynqmp = " \
	file://0001-zynqmp-Add-custom-default-env-settings.patch \
	file://0003-zynqmp-Use-fixed-env-location-depending-on-build-tim.patch \
"

SRC_URI_append_damc-fmc1z7io = " \
	file://0002-xilinx-add-support-for-EEPROM-with-16-bit-addr.patch \
"

do_configure_append() {
    cp ${B}/../custom_default_env.h ${S}/include
}
