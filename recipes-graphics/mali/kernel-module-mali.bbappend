FILESEXTRAPATHS_append := "${THISDIR}/kernel-module-mali:"
SRC_URI_append = " \
	file://0100-Don-t-expect-to-receive-nonzero-dma_handle-from-kern.patch \
"

# EXTRA_OEMAKE_append = " \
#     BUILD=debug     \
#     MALI_QUIET=0    \
# "
