DESCRIPTION = "DMMC-STAMP Mailbox tools"
LICENSE = "CLOSED"
PV = "0.0.1"

SRCREV = "507a17f57e14f0e2bc3ba2bc1657343f9ca872be"
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
