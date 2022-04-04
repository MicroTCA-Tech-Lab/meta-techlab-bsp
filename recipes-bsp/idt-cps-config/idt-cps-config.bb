CRIPTION = "Configuration tool for IDT crosspoint switch"
LICENSE = "CLOSED"
PV = "1.0"
PR = "r2"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

S = "${WORKDIR}"

SRC_URI = " \
    file://setup.py \
    file://idt-cps-config.py \
    file://idtcpsconfig/config.py \
    file://idtcpsconfig/IdtCpsConfig.py \
    file://idtcpsconfig/__init__.py \
    file://idtcpsconfig/PortConfig.py \
    file://idtcpsconfig/ZupPortName.py \
    file://idt-cps-init.sh \
"

RDEPENDS_${PN} = "python3 python3-smbus i2c-bus-locator"

inherit setuptools3


do_install_append() {
    # init script to program the CPS at the startup
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d

    install -m 0755 ${WORKDIR}/idt-cps-init.sh  ${D}${sysconfdir}/init.d/

    ln -sf ../init.d/idt-cps-init.sh ${D}${sysconfdir}/rcS.d/S82idt-cps-init
}
