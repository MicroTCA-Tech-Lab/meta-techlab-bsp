DESCRIPTION = "DAMC-FMC2ZUP minimal recovery image for use as initramfs"

require ./recipes-core/images/petalinux-image-minimal.bb

IMAGE_FSTYPES_remove = "ext3 ext4 wic.qemu-sd jffs2 tar.gz"

INITRAMFS_IMAGE_BUNDLE = "0"

# To build this along zup-image-demo(-full), add INITRAMFS_IMAGE = "zup-recovery" to local.conf
