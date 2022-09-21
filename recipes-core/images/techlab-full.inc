require recipes-core/images/petalinux-image-full.bb

IMAGE_INSTALL_append = " packagegroup-techlab-devbox"
IMAGE_INSTALL_append = " packagegroup-locale-support"
IMAGE_INSTALL_append = " packagegroup-recovery-support"

IMAGE_FEATURES_remove = " petalinux-vitisai petalinux-openamp"

inherit extrausers
EXTRA_USERS_PARAMS = "usermod -s /bin/zsh root"