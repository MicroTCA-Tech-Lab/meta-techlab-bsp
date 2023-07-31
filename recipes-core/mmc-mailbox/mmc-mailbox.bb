DESCRIPTION = "DMMC-STAMP Mailbox support"
LICENSE = "BSD"
PV = "1.0.2"

SRCREV = "fef16a5652b4d18277032fa0426eac2250c65397"
SRC_URI = "git://git@github.com/MicroTCA-Tech-Lab/mmc-mailbox.git;protocol=ssh"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=750d848625d8174091b953f2de0e8f8e"

SRC_URI += "\
  file://init.d/mmcctrld \
"

RDEPENDS_${PN} = "mmc-mailbox-driver"

S = "${WORKDIR}/git"

INITSCRIPT_NAME = "mmcctrld"
# The 90 is to explicitly start after syslogd, b/c update-rc.d ignores the syslog dependency for some reason
INITSCRIPT_PARAMS = "defaults 90"

inherit cmake update-rc.d

do_install_append() {
  install -d ${D}${sysconfdir}/init.d
  install -m 0755 ${WORKDIR}/init.d/mmcctrld  ${D}${sysconfdir}/init.d/
}
