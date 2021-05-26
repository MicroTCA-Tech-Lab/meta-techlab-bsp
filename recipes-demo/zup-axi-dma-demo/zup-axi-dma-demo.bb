DESCRIPTION = "AXI DMA demo"
LICENSE = "CLOSED"
PV = "0.8.0"
PR = "r0"

DEPENDS = "boost"
RDEPENDS_${PN} = "boost-log boost-program-options"

inherit pkgconfig cmake

SRC_URI = " \
    file://zup-axi-dma-demo_v${PV}.tar.gz \
"

EXTRA_OECMAKE += "-DCMAKE_SKIP_RPATH=TRUE"

S="${WORKDIR}"

do_install() {
    # library
    install -m 0755 -d ${D}${libdir}
    oe_libinstall -C ${S}/build -so libudmaio ${D}${libdir}

    # example
    install -d ${D}${bindir}
    install -m 0755 axi_dma_demo ${D}${bindir}
}
