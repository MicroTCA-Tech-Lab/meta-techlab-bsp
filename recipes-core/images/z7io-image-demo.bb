DESCRIPTION = "DAMC-FMC1Z7IO Small Linux Image"

require ./recipes-core/images/petalinux-image-minimal.bb

require z7io-common.inc

EXTRA_IMAGE_FEATURES += " package-management "
