COMPATIBLE_MACHINE = "damc-fmc2zup"

require techlab-common.inc

IMAGE_INSTALL_append = " packagegroup-zup-support"
IMAGE_INSTALL_append = " packagegroup-zup-demo"
