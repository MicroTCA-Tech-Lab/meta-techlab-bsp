CRIPTION = "udmabuf(User space mappable DMA Buffer)"
LICENSE = "BSD"
PV = "2.1.2"
PR = "r0"

#SRC_URI = "git://github.com/ikwzm/udmabuf.git;protocol=git;tag=v2.1.2"
SRCREV = "${AUTOREV}"
SRC_URI = "git://github.com/ikwzm/udmabuf.git"
#SRC_URI[sha256sum] = "ad96c798ed85ec61de4cd7e32b5939a793d7bd0ec09614db7d02ab7e033a0ce7"

LIC_FILES_CHKSUM = "file://LICENSE;md5=bebf0492502927bef0741aa04d1f35f5" 

S = "${WORKDIR}/git"

inherit module

# https://lists.yoctoproject.org/pipermail/meta-intel/2018-September/005546.html
DEPENDS += "xz-native bc-native bison-native"

# patches
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI_append = " file://0001-Update-Makefile-for-Yocto-env-variables.patch \
    file://udmabuf.sh \
"

FILES_${PN} = " \
    /etc/rcS.d/S80udmabuf \
    /etc/init.d/udmabuf.sh \
"

do_install_append() {
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d

    install -m 0755 ${WORKDIR}/udmabuf.sh  ${D}${sysconfdir}/init.d/

    ln -sf ../init.d/udmabuf.sh  ${D}${sysconfdir}/rcS.d/S80udmabuf
}
