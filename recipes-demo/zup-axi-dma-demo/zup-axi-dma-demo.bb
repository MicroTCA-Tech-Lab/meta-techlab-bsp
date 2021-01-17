DESCRIPTION = "AXI DMA demo"
LICENSE = "CLOSED"
PV = "0.1"
PR = "r0"

DEPENDS = "boost"
RDEPENDS_${PN} = "boost-log"

inherit pkgconfig cmake

SRC_URI = " \
	file://CMakeLists.txt \
	file://inc/UDmaBuf.hpp \
	file://inc/UioAxiDmaIf.hpp \
	file://inc/UioIfFactory.hpp \
	file://inc/UioIf.hpp \
	file://inc/UioMemSgdma.hpp \
	file://inc/UioTrafficGen.hpp \
	file://src/axi_dma_demo.cpp \
	file://src/UDmaBuf.cpp \
	file://src/UioAxiDmaIf.cpp \
	file://src/UioMemSgdma.cpp \
	file://src/UioTrafficGen.cpp \
"
S="${WORKDIR}"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 axi_dma_demo ${D}${bindir}
}

