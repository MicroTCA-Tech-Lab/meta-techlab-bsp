DESCRIPTION = "DAMC-FMC1Z7IO Full Linux Image"

IMAGE_AUTOLOGIN = "0"

require ./recipes-core/images/petalinux-image-full.bb

require z7io-common.inc

IMAGE_INSTALL_append = " packagegroup-techlab-devbox"
IMAGE_INSTALL_append = " packagegroup-locale-support"
IMAGE_INSTALL_append = " packagegroup-recovery-support"

inherit extrausers
EXTRA_USERS_PARAMS = "usermod -s /bin/zsh root"

IMAGE_FEATURES_remove = " petalinux-vitisai petalinux-openamp"
