
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI_append = " \
	file://0001-net-macb-enable-support-for-fibre-PHYs.patch \
	file://clk-si5341.patch \
	file://clk_si5341.cfg \
"
