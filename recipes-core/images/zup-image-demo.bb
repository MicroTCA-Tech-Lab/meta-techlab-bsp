DESCRIPTION = "Demo for DAMC-FMC2ZUP"

require ./recipes-core/images/petalinux-image-minimal.bb

require zup-common.inc

IMAGE_FSTYPES_remove = "cpio.gz cpio cpio.gz.u-boot cpio.bz2 ext3 ext4 wic.qemu-sd"

EXTRA_IMAGE_FEATURES += " package-management "

IMAGE_INSTALL_append = " htop"
IMAGE_INSTALL_append = " nano"
IMAGE_INSTALL_append = " python3"
IMAGE_INSTALL_append = " vim"
IMAGE_INSTALL_append = " udmabuf"