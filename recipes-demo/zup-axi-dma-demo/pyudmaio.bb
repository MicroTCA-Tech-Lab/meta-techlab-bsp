DESCRIPTION = "AXI DMA demo"
LICENSE = "CLOSED"
PV = "0.8.7"
PR = "r0"

# pybind11 should be version 2.6 or higher
#  - Bitbake does not respect version specification (e.g. "(>= 2.6)")
DEPENDS = "libudmaio python3-pybind11-native (>= 2.6)"
RDEPENDS_${PN} = "libudmaio python3-pybind11 (>= 2.6) python3-bitstruct"

inherit pypi setuptools3

SRC_URI = " \
    file://zup-axi-dma-demo_v${PV}.tar.gz \
"

S="${WORKDIR}/pyudmaio"
