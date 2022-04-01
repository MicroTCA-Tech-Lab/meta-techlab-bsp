DESCRIPTION = "DAMC-FMC2ZUP Small Linux Image"

require ./recipes-core/images/petalinux-image-minimal.bb

require zup-common.inc

EXTRA_IMAGE_FEATURES += " package-management "
