DESCRIPTION = "AXI DMA demo"
LICENSE = "CLOSED"
PV = "0.8.7"
PR = "r0"

DEPENDS = "boost libudmaio"
RDEPENDS_${PN} = "boost-log boost-program-options libudmaio"

inherit pkgconfig cmake

SRC_URI = " \
    file://zup-axi-dma-demo_v${PV}.tar.gz \
"

EXTRA_OECMAKE += "-DCMAKE_SKIP_RPATH=TRUE"

S="${WORKDIR}"

do_install() {
    # example
    install -d ${D}${bindir}
    install -m 0755 axi_dma_demo_cpp ${D}${bindir}
}
