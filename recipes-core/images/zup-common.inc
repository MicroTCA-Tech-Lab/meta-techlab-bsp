
# here we include basic packages needed for the ZUP.
# these packages are included regardless of the application.

# Generic Linux applications
IMAGE_INSTALL_append = " htop"
IMAGE_INSTALL_append = " nano"
IMAGE_INSTALL_append = " python3"
IMAGE_INSTALL_append = " vim"

# Generic Linux HW interface tools
IMAGE_INSTALL_append = " ethtool"
IMAGE_INSTALL_append = " i2c-tools"
IMAGE_INSTALL_append = " phytool"

# TechLab tools
IMAGE_INSTALL_append = " udmabuf"
IMAGE_INSTALL_append = " pyudmaio"
IMAGE_INSTALL_append = " lsuio"

# ZUP specific recipes
IMAGE_INSTALL_append = " si-labs-clk-config"
IMAGE_INSTALL_append = " fw-plreset"
IMAGE_INSTALL_append = " idt-cps-config"
IMAGE_INSTALL_append = " uio-users-group uio-users-udev-rule"

# ZUP demos
IMAGE_INSTALL_append = " zup-axi-dma-demo"
IMAGE_INSTALL_append = " clock-monitor"
IMAGE_INSTALL_append = " irq-handler-demo"

# install if fpga-manager is enabled
IMAGE_INSTALL_append = " ${@'fpgautil-init' if d.getVar('FPGA_MNGR_RECONFIG_ENABLE') == '1' else ''}"

# remove unused image types
IMAGE_FSTYPES_remove = "cpio.gz cpio cpio.gz.u-boot cpio.bz2 ext3 ext4 wic.qemu-sd jffs2"

# TOOLCHAIN_TARGET_TASK_append = " kernel-devsrc"

# Couldn't make Dropbear work with pam_group and pam_mkhomedir
IMAGE_FEATURES += "${@bb.utils.contains('DISTRO_FEATURES', 'desy-login-support', ' ssh-server-openssh', '' ,d)}"
