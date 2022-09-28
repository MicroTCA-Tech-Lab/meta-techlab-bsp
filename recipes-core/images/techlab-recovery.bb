DESCRIPTION = "Minimal recovery image for use as initramfs"

require recipes-core/images/petalinux-image-minimal.bb

IMAGE_FSTYPES_remove = "ext3 ext4 wic.qemu-sd jffs2 tar.gz"
IMAGE_INSTALL_append = " packagegroup-recovery-support"
IMAGE_INSTALL_append = " vim-tiny"

IMAGE_INSTALL_remove = "fpgautil-init external-hdf"
IMAGE_FEATURES_remove = "fpga-manager"

INITRAMFS_IMAGE_BUNDLE = "0"

# To build this along (zup|z7io)-image-demo(-full), add INITRAMFS_IMAGE = "techlab-recovery" to local.conf
