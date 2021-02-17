CRIPTION = "Locate I2C bus based on compatible string and/or address"
LICENSE = "CLOSED"
PV = "1.1"
PR = "r0"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

S = "${WORKDIR}"

SRC_URI = " \
    file://setup.py \
    file://i2c_bus_locator/__init__.py \
"

RDEPENDS_${PN} = "python3"

inherit setuptools3

