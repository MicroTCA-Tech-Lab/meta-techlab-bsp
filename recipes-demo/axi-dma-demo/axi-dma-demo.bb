COMPATIBLE_MACHINE = "damc-fmc1z7io|damc-fmc2zup"

DESCRIPTION = "AXI DMA demo"
LICENSE = "CLOSED"
PV = "0.9.3"
PR = "r0"

DEPENDS = "boost libudmaio"
RDEPENDS_${PN} = "boost-log boost-program-options libudmaio"

inherit pkgconfig cmake

SRCREV = "c7fcc77fd2cf9990c77d4e0bde59c650bf71aa0d"
SRC_URI = "git://github.com/MicroTCA-Tech-Lab/libudmaio.git;protocol=https"

EXTRA_OECMAKE_damc-fmc2zup = "-DCMAKE_SKIP_RPATH=TRUE -DTARGET_HW=ZUP"
EXTRA_OECMAKE_damc-fmc1z7io = "-DCMAKE_SKIP_RPATH=TRUE -DTARGET_HW=Z7IO"

S="${WORKDIR}/git"

do_install() {
    # example
    install -d ${D}${bindir}
    install -m 0755 axi_dma_demo_cpp ${D}${bindir}
}
