
# here we include basic packages needed for the ZUP.
# these packages are included regardless of the application.

IMAGE_INSTALL_append = " ethtool"
IMAGE_INSTALL_append = " i2c-tools"
IMAGE_INSTALL_append = " phytool"
IMAGE_INSTALL_append = " si-labs-clk-config"
IMAGE_INSTALL_append = " fw-plreset"
IMAGE_INSTALL_append = " uio-users-group uio-users-udev-rule"
