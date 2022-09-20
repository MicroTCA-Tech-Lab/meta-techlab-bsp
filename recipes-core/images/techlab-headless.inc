require ./recipes-core/images/petalinux-image-minimal.bb

IMAGE_FEATURES_append = " \
    petalinux-base \
    petalinux-networking-stack \
    petalinux-utils \
    dev-pkgs \
    tools-sdk \
"

IMAGE_INSTALL_append = " git python3-pip haveged"
IMAGE_INSTALL_append = " util-linux glibc-utils sudo"

IMAGE_INSTALL_append = " packagegroup-techlab-devbox"
IMAGE_INSTALL_append = " packagegroup-locale-support"
IMAGE_INSTALL_append = " packagegroup-recovery-support"

inherit extrausers
EXTRA_USERS_PARAMS = "usermod -s /bin/zsh root"
