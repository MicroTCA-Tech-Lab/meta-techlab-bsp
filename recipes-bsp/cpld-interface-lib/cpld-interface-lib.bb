COMPATIBLE_MACHINE = "damc-fmc1z7io"

DESCRIPTION = "Libray for interfacing Z7IO CPLD for FP_IO and MLVDS control"
LICENSE = "CLOSED"
PV = "1.2"
PR = "r1"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

S = "${WORKDIR}"

SRC_URI = " \
    file://cpld_interface_lib/__init__.py \
    file://cpld_interface_lib/CpldInterface.py \
    file://cpld_interface_lib/CpldSpiDriver.py \
    file://cpld_interface_lib/FPIOCtrl.py \
    file://cpld_interface_lib/MLVDSCtrl.py \
    file://setup.py \
"

RDEPENDS_${PN} = "python3 python3-spidev python3-bitstring"

inherit setuptools3
