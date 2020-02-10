DESCRIPTION = "Hello world style project"

require ./recipes-core/images/petalinux-image-minimal.bb

IMAGE_FSTYPES_remove = "cpio.gz cpio cpio.gz.u-boot cpio.bz2 ext3 ext4 wic.qemu-sd"

IMAGE_INSTALL_append = " ethtool"
IMAGE_INSTALL_append = " vim"
