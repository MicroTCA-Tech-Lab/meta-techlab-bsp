DESCRIPTION = "Minimal + some useful tools"

require ./zup-image-minimal.bb

IMAGE_INSTALL_append = " ethtool"
IMAGE_INSTALL_append = " htop"
IMAGE_INSTALL_append = " i2c-tools"
IMAGE_INSTALL_append = " nano"
IMAGE_INSTALL_append = " phytool"
IMAGE_INSTALL_append = " python3"
IMAGE_INSTALL_append = " vim"
