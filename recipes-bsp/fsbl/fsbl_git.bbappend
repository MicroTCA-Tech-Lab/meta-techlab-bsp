
XSCTH_APP_COMPILER_FLAGS_append_damc-fmc2zup = " -DFSBL_DEBUG"

FILESEXTRAPATHS_prepend_damc-fmc2zup := "${THISDIR}/files/fmc2zup:"
SRC_URI += " file://0001-Enable-debug-add-additional-info-to-print.patch "
