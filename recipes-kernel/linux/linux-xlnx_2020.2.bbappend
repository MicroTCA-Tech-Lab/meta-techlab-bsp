FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append_damc-fmc2zup = " \
	file://usb.cfg \
	file://fpga-debugfs.cfg \
    file://0001-Allow-reading-the-ZynqMP-IDCODE.patch \
"

SRC_URI_append_damc-fmc1z7io = " \
    file://gpio_PCA953X.cfg \
    file://spi_SPIDEV.cfg \
    file://dma_ADI_AXI-DMAC.cfg \
    file://xilinx_DRM.cfg \
    file://fpga-debugfs.cfg \
    file://0001-adi-hdmi-output-adi-axi-common.patch \
"
