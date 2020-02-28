DESCRIPTION = "Minimal + some useful tools"

require ./zup-image-minimal.bb

EXTRA_IMAGE_FEATURES += " package-management "

IMAGE_INSTALL_append = " ethtool"
IMAGE_INSTALL_append = " htop"
IMAGE_INSTALL_append = " i2c-tools"
IMAGE_INSTALL_append = " nano"
IMAGE_INSTALL_append = " phytool"
IMAGE_INSTALL_append = " python3"
IMAGE_INSTALL_append = " vim"
IMAGE_INSTALL_append = " si-labs-clk-config"
IMAGE_INSTALL_append = " usb-c-pd-programmer"
