// clang-format off

#undef CONFIG_EXTRA_ENV_SETTINGS
#define CONFIG_EXTRA_ENV_SETTINGS                                              \
	"fdt_high=10000000\0" \
	"fdt_addr_r=0x40000000\0" \
	"fdt_size_r=0x00040000\0" \
	"kernel_addr_r=0x18000000\0" \
	"kernel_size_r=0x02000000\0" \
	"scriptaddr=0x20000000\0" \
	"ramdisk_addr_r=0x02100000\0" \
	"ramdisk_size_r=0x05D80000\0" \
	"script_size_f=0x80000\0" \
  "bootargs_common='earlycon clk_ignore_unused rw rootwait cpuidle.off=1 uio_pdrv_genirq.of_id=\"generic-uio\" video=DP-1'\0" \
  "sd_load_dtb_img=fatload mmc 0 ${fdt_addr_r} damc-motctrl-system.dtb && fatload mmc 0 ${kernel_addr_r} Image\0"                   \
  "emmc_load_dtb_img=fatload mmc 1 ${fdt_addr_r} damc-motctrl-system.dtb && fatload mmc 1 ${kernel_addr_r} Image\0"                 \
  "qspi_load_dtb_img=sf probe 0 0 0 && sf read ${fdt_addr_r} 0x00240000 ${fdt_size_r} && sf read ${kernel_addr_r} 0x00280000 ${kernel_size_r}\0" \
  "qspi_load_ramdisk=sf read ${ramdisk_addr_r} 0x02280000 ${ramdisk_size_r}\0"                                                                \
  "kernel_start_noramdisk=booti ${kernel_addr_r} - ${fdt_addr_r}\0"                                                                    \
  "kernel_start_ramdisk=booti ${kernel_addr_r} ${ramdisk_addr_r} ${fdt_addr_r}\0"                                                      \
  "boot_mmc0=echo DAMC-MOTCTRL SD boot script && run sd_load_dtb_img && setenv bootargs root=/dev/mmcblk0p2 ${bootargs_common} && run kernel_start_noramdisk\0"            \
  "boot_qspi0=echo DAMC-MOTCTRL eMMC boot script && run emmc_load_dtb_img && setenv bootargs root=/dev/mmcblk1p2 ${bootargs_common} && run kernel_start_noramdisk\0"            \
  "boot_net=echo DAMC-MOTCTRL QSPI/NFS boot script && run qspi_load_dtb_img && setenv bootargs root=/dev/nfs nfsroot=${nfsserver}:${nfsroot},nfsvers=3 ip=dhcp ${bootargs_common} && run kernel_start_noramdisk\0" \
  "boot_recovery=echo DAMC-MOTCTRL QSPI/initramfs boot script && run qspi_load_dtb_img && run qspi_load_ramdisk && setenv bootargs root=/dev/ram0 ${bootargs_common} && run kernel_start_ramdisk\0" \
  "nfsserver=192.168.1.92\0"            \
  "nfsroot=/nfsroot/motctrl\0"             \
  "boot_targets=recovery\0"             \
  "distro_bootcmd=for target in ${boot_targets}; do run boot_${target}; done\0" \
