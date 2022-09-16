DESCRIPTION = "DAMC-FMC1Z7IO Headless Linux Image"

IMAGE_AUTOLOGIN = "0"

require ./recipes-core/images/petalinux-image-minimal.bb

require z7io-common.inc

IMAGE_FEATURES_append = " \
    package-management \
    petalinux-base \
    petalinux-networking-stack \
    petalinux-utils \
    "

IMAGE_INSTALL_append = " haveged"
IMAGE_INSTALL_append = " util-linux glibc-utils sudo"
IMAGE_INSTALL_append = " packagegroup-techlab-devbox"
IMAGE_INSTALL_append = " packagegroup-locale-support"
IMAGE_INSTALL_append = " packagegroup-recovery-support"

inherit extrausers
EXTRA_USERS_PARAMS = "usermod -s /bin/zsh root"
