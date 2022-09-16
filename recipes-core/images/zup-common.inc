COMPATIBLE_MACHINE = "damc-fmc2zup"

# here we include basic packages needed for the ZUP.
# these packages are included regardless of the application.

# Generic Linux applications
IMAGE_INSTALL_append = " htop"
IMAGE_INSTALL_append = " nano"
IMAGE_INSTALL_append = " python3"
IMAGE_INSTALL_append = " vim"

IMAGE_INSTALL_append = " packagegroup-hwtools"
IMAGE_INSTALL_append = " packagegroup-zup-support"
IMAGE_INSTALL_append = " packagegroup-zup-demo"

# install if fpga-manager is enabled
IMAGE_INSTALL_append = " ${@'fpgautil-init' if d.getVar('FPGA_MNGR_RECONFIG_ENABLE') == '1' else ''}"

# remove unused image types
IMAGE_FSTYPES_remove = "cpio.gz cpio cpio.gz.u-boot cpio.bz2 ext3 ext4 wic.qemu-sd jffs2"

# TOOLCHAIN_TARGET_TASK_append = " kernel-devsrc"

# Couldn't make Dropbear work with pam_group and pam_mkhomedir
IMAGE_FEATURES += "${@bb.utils.contains('DISTRO_FEATURES', 'desy-login-support', ' ssh-server-openssh', '' ,d)}"
