CRIPTION = "Configuration tool for Si Labs chips on I2C bus"
LICENSE = "CLOSED"
PV = "1.0"
PR = "r1"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

S = "${WORKDIR}"

SRC_URI = " \
    file://setup.py \
    file://si-labs-clk-config.py \
    file://slcc/extra_logging.py \
    file://slcc/Si5341driver.py \
    file://slcc/SiLabsTxtParser.py \
"

RDEPENDS_${PN} = "python python3-smbus"

inherit setuptools3
