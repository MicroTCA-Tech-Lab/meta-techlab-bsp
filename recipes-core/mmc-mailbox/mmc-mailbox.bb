DESCRIPTION = "DMMC-STAMP Mailbox tools"
LICENSE = "CLOSED"
PV = "0.0.1"

SRCREV = "a46be18e8cd85ecf3990c3c97d0c2f49c81ed32e"
SRC_URI = "git://git@msktechvcs.desy.de/huesmann/mmc-mailbox.git;protocol=ssh"

SRC_URI += "\
  file://init.d/mmcctrld \
"

RDEPENDS_${PN} = "mmc-mailbox-driver"

S = "${WORKDIR}/git"

INITSCRIPT_NAME = "mmcctrld"
# The 90 is to explicitly start after syslogd, b/c update-rc.d ignores the syslog dependency for some reason
INITSCRIPT_PARAMS = "defaults 90"

inherit cmake update-rc.d

# MMC mailbox location on ZUP
EXTRA_OECMAKE += "-DADAPTER_DT_NAME=iic_axi_iic_mmc -DI2C_ADDR=002a"

do_install_append() {
  install -d ${D}${sysconfdir}/init.d
  install -m 0755 ${WORKDIR}/init.d/mmcctrld  ${D}${sysconfdir}/init.d/
}
