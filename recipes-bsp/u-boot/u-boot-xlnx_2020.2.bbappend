FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " \
	file://env-in-qspi.cfg \
	file://custom_default_env.h \
	file://eth-backplane/marvell-reg-init.patch \
	file://eth-backplane/0001-Use-PHY-Fiber-interface.patch \
	file://0002-xilinx-enable-debug-for-MAC-addr-read.patch \
	file://0003-Add-custom-default-env-settings.patch \
"

SRC_URI_append_damc-fmc2zup = " \
	file://0001-Revert-arm64-zynqmp-Remove-all-Xilinx-private-comman.patch \
"

SRC_URI_append_damc-fmc1z7io = " \
	file://0002-xilinx-add-support-for-EEPROM-with-16-bit-addr.patch \
	file://0003-Override-CONFIG_EXTRA_ENV_SETTINGS.patch \
"

SRC_URI_append_damc-motctrl = " \
	file://0001-Revert-arm64-zynqmp-Remove-all-Xilinx-private-comman.patch \
	file://mmcmailbox/0004-Add-support-for-MMC-mailbox.patch \
	file://0005-Disable-PHY-init.patch \
	file://0006-Fix-moca-phy-mode.patch \
	file://0007-Ignore-secondary-NICs.patch \
	file://enable-i2c-gpio.cfg \
"

SRC_URI_append_damc-unizup = " \
	file://mmcmailbox/0004-Add-support-for-MMC-mailbox.patch \
	file://mmcmailbox/enable-i2c-cdns.cfg \
	file://mmcmailbox/mac-addr.cfg \
"

do_configure_append() {
    cp ${B}/../custom_default_env.h ${S}/include
}
