DESCRIPTION = "DMMC-STAMP Mailbox tools"
LICENSE = "CLOSED"
PV = "0.0.1"

RDEPENDS_${PN} = "mmc-mailbox-driver"

SRC_URI = "\
  file://CMakeLists.txt \
  file://mmcmb/fpga_mailbox_layout.h \
  file://mmcmb/mmcmb.h \
  file://mmcctrld.c \
  file://mmcinfo.c \
  file://mmcmb.c \
  file://init.d/mmcctrld \
"
S = "${WORKDIR}"

inherit cmake

# MMC mailbox location on ZUP
EXTRA_OECMAKE += "-DMAILBOX_FILE=/sys/bus/i2c/devices/5-002a/eeprom"

do_install_append() {
  install -d ${D}${sysconfdir}/init.d
  install -d ${D}${sysconfdir}/rcS.d
  install -m 0755 ${WORKDIR}/init.d/mmcctrld  ${D}${sysconfdir}/init.d/
  # Start after S50fpgautil-init
  ln -sf ../init.d/mmcctrld  ${D}${sysconfdir}/rcS.d/S51mmcctrld
}
