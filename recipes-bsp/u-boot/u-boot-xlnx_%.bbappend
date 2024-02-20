FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " \
	file://custom_default_env.h \
	file://custom-default-env-h.patch \
	file://enable-debug-for-MAC-addr-read.patch \
	file://env-in-qspi.cfg \
	file://eth-backplane/marvell-reg-init.patch \
	file://eth-backplane/Use-PHY-Fiber-interface.patch \
	file://fixed-env-location.patch \
	file://tftp-port.patch \
"

SRC_URI_append_damc-fmc2zup = " \
	file://mac-addr.cfg \
"

SRC_URI_append_damc-fmc1z7io = " \
	file://eeprom-16-bit.patch \
	file://mac-addr.cfg \
"

SRC_URI_append_damc-motctrl = " \
	file://Disable-PHY-init.patch \
	file://Fix-moca-phy-mode.patch \
	file://Ignore-secondary-NICs.patch \
	file://mmcmailbox/enable-i2c-gpio.cfg \
	file://mmcmailbox/Add-support-for-MMC-mailbox.patch \
	file://mmcmailbox/mac-addr.cfg \
"

SRC_URI_append_damc-unizup = " \
	file://mmcmailbox/enable-i2c-cdns.cfg \
	file://mmcmailbox/Add-support-for-MMC-mailbox.patch \
	file://mmcmailbox/mac-addr.cfg \
"

do_configure_append() {
    cp ${B}/../custom_default_env.h ${S}/include
}
