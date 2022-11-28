# here we include basic packages needed for TechLab hardware.
# these packages are included regardless of the application.

# Generic Linux applications
IMAGE_INSTALL_append = " htop nano python3 vim"

# Misc. hardware tools
IMAGE_INSTALL_append = " packagegroup-hwtools"

# TechLab specific applications
IMAGE_INSTALL_append = " mmc-mailbox"

# Install 'fpgautil-init' if fpga-manager is enabled
IMAGE_INSTALL_append = " ${@'fpgautil-init' if d.getVar('FPGA_MNGR_RECONFIG_ENABLE') == '1' else ''}"

# Remove unused image types
IMAGE_FSTYPES_remove = "cpio.gz cpio cpio.gz.u-boot cpio.bz2 ext3 ext4 wic.qemu-sd jffs2"

# Use real sshd instead of dropbear
IMAGE_FEATURES += ' ssh-server-openssh'

# Enable package management for all image types except recovery
IMAGE_FEATURES += ' package-management'

# Enter machine & image name into custom banners
MACH_UPPER = "${@d.getVar('MACHINE').upper()}"
fixup_custom_banners() {
    sed -i 's/MACHINE/${MACH_UPPER}/g' ${IMAGE_ROOTFS}/etc/issue
    sed -i 's/MACHINE/${MACH_UPPER}/g' ${IMAGE_ROOTFS}/etc/banner
    sed -i 's/IMAGE/${IMAGE_BASENAME}/g' ${IMAGE_ROOTFS}/etc/issue
    sed -i 's/IMAGE/${IMAGE_BASENAME}/g' ${IMAGE_ROOTFS}/etc/banner
}
ROOTFS_POSTPROCESS_COMMAND += "fixup_custom_banners; "

# Gather version information into /etc/build
inherit image-buildinfo-mod
IMAGE_BUILDINFO_VARS = "DISTRO_VERSION MACHINE IMAGE_BASENAME BUILDNAME"
