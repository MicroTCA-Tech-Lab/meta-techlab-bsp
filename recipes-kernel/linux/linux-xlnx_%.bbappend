FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " \
    file://enable-RTL8153.cfg \
"

SRC_URI_append_damc-fmc2zup = " \
    file://usb.cfg \
    file://fpga-debugfs.cfg \
    file://0001-Allow-reading-the-ZynqMP-IDCODE_${LINUX_VERSION}.patch \
"

SRC_URI_append_damc-fmc1z7io = " \
    file://gpio_PCA953X.cfg \
    file://spi_SPIDEV.cfg \
    file://dma_ADI_AXI-DMAC.cfg \
    file://xilinx_DRM.cfg \
    file://fpga-debugfs.cfg \
    file://0001-adi-hdmi-output-adi-axi-common.patch \
"

SRC_URI_append_damc-motctrl = " \
    file://usb.cfg \
    file://fpga-debugfs.cfg \
    file://0001-Allow-reading-the-ZynqMP-IDCODE_${LINUX_VERSION}.patch \
    file://0002-Add-internal_pcspma-mode.patch \
    file://0003-Support-NIC-numbering-from-DT-aliases.patch \
    file://i2c_gpio.cfg \
"

SRC_URI_append_damc-unizup = " \
    file://usb.cfg \
    file://fpga-debugfs.cfg \
    file://0001-Allow-reading-the-ZynqMP-IDCODE_${LINUX_VERSION}.patch \
"
