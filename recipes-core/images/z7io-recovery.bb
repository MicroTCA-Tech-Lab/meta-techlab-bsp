DESCRIPTION = "DAMC-FMC1Z7IO minimal recovery image for use as initramfs"

require ./recipes-core/images/petalinux-image-minimal.bb

IMAGE_FSTYPES_remove = "ext3 ext4 wic.qemu-sd jffs2 tar.gz"
IMAGE_INSTALL_append = " packagegroup-recovery-support"
IMAGE_INSTALL_append = " vim-tiny"

INITRAMFS_IMAGE_BUNDLE = "0"

# To build this along z7io-image-demo(-full), add INITRAMFS_IMAGE = "z7io-recovery" to local.conf
