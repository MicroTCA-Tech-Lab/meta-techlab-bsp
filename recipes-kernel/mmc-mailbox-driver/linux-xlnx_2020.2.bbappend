# Disable pm_power_off for psci driver, make sure that mmc-mailbox-driver can use it instead

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI_append = " \
	file://0001-Leave-pm_power_off-to-MMC-mailbox-driver.patch \
"
