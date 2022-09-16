
XSCTH_APP_COMPILER_FLAGS_append_damc-fmc2zup = " -DFSBL_DEBUG"
XSCTH_APP_COMPILER_FLAGS_append_damc-fmc1z7io = " -DFSBL_DEBUG"

FILESEXTRAPATHS_prepend_damc-fmc2zup := "${THISDIR}/files/fmc2zup:"
FILESEXTRAPATHS_prepend_damc-fmc1z7io := "${THISDIR}/files/fmc1z7io:"

SRC_URI_append_damc-fmc2zup = "\
    file://0001-Enable-debug-add-additional-info-to-print.patch \
"

SRC_URI_append_damc-fmc1z7io = "\
    file://0001-Add-board-specific-lines.patch \
    file://0002-Force-single-SPI-mode-dirty-hack.patch \
"
