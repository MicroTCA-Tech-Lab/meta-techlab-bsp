DESCRIPTION = "Userspace DMA I/O library"
LICENSE = "CLOSED"
PV = "0.8.7"
PR = "r0"

DEPENDS = "boost"
RDEPENDS_${PN} = "boost-log boost-program-options"

inherit pkgconfig cmake

SRC_URI = " \
    file://zup-axi-dma-demo_v${PV}.tar.gz \
"

EXTRA_OECMAKE += "-DCMAKE_SKIP_RPATH=TRUE"

S="${WORKDIR}"
