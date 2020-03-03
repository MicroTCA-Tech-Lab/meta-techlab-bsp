CRIPTION = "Programming tool for USB-C PD chip on I2C bus"
LICENSE = "CLOSED"
PV = "1.0.1"
PR = "r0"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

S = "${WORKDIR}"

SRC_URI = " \
    file://setup.py \
    file://usb-c-pd-programmer.py \
"


RDEPENDS_${PN} = "python python3-smbus"

inherit setuptools3
