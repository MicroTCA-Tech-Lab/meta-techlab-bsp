XSCTH_APP_COMPILER_FLAGS_append = " -DFSBL_DEBUG"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append_damc-fmc2zup = "\
    file://0001-Enable-debug-add-additional-info-to-print.patch \
"

SRC_URI_append_damc-fmc1z7io = "\
    file://0001-Add-board-specific-lines.patch \
    file://0002-Force-single-SPI-mode-dirty-hack.patch \
"
