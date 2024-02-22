# Enable SD3.0 UHS mode for Unizup
XSCTH_APP_COMPILER_FLAGS_append_damc-unizup = " -DUHS_MODE_ENABLE"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append_damc-fmc2zup = "\
    file://0001-Enable-debug-add-additional-info-to-print.patch \
"

SRC_URI_append_damc-fmc1z7io = "\
    file://0001-Add-board-specific-lines.patch \
    file://0002-Force-single-SPI-mode-dirty-hack.patch \
"

SRC_URI_append_damc-motctrl = "\
    file://0001-Add-board-specific-lines.patch \
    file://0002-Force-single-SPI-mode-dirty-hack.patch \
"
