DESCRIPTION = "DMMC-STAMP Mailbox tools"
LICENSE = "CLOSED"
PV = "0.0.1"

SRCREV = "e782d1009a5a4e3fb3fb194d9e10e41daa7af5ad"
SRC_URI = "git://git@msktechvcs.desy.de/huesmann/mmc-mailbox.git;protocol=ssh"

SRC_URI += "\
  file://init.d/mmcctrld \
"

RDEPENDS_${PN} = "mmc-mailbox-driver"

S = "${WORKDIR}/git"

inherit cmake

# MMC mailbox location on ZUP
EXTRA_OECMAKE += "-DADAPTER_DT_NAME=iic_axi_iic_mmc -DI2C_ADDR=002a"

do_install_append() {
  install -d ${D}${sysconfdir}/init.d
  install -d ${D}${sysconfdir}/rcS.d
  install -m 0755 ${WORKDIR}/init.d/mmcctrld  ${D}${sysconfdir}/init.d/
  # Start after S50fpgautil-init
  ln -sf ../init.d/mmcctrld  ${D}${sysconfdir}/rcS.d/S51mmcctrld
}
