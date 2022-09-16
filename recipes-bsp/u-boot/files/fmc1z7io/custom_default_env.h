// clang-format off

#undef CONFIG_EXTRA_ENV_SETTINGS
#define CONFIG_EXTRA_ENV_SETTINGS                                              \
  "fdt_high=0x20000000\0"                                                      \
  "initrd_high=0x20000000\0"                                                   \
  "scriptaddr=0x20000\0"                                                       \
  "script_size_f=0x40000\0"                                                    \
  "fdt_addr_r=0x1f00000\0"                                                     \
  "pxefile_addr_r=0x2000000\0"                                                 \
  "kernel_addr_r=0x2000000\0"                                                  \
  "scriptaddr=0x3000000\0"                                                     \
  "ramdisk_addr_r=0x3100000\0"                                                 \
  "bootargs_common='earlyprintk console=ttyPS0,115200 rw rootwait cpuidle.off=1 uio_pdrv_genirq.of_id=\"generic-uio\" cma=64M'\0"      \
  "sd_load_dtb_uimg=fatload mmc 0 ${fdt_addr_r} damc-fmc1z7io-system.dtb && fatload mmc 0 ${kernel_addr_r} uImage\0"                   \
  "emmc_load_dtb_uimg=fatload mmc 1 ${fdt_addr_r} damc-fmc1z7io-system.dtb && fatload mmc 1 ${kernel_addr_r} uImage\0"                   \
  "qspi_load_dtb_uimg=sf probe 0 0 0 && sf read ${fdt_addr_r} 0x00240000 0x00040000 && sf read ${kernel_addr_r} 0x00280000 0x800000\0" \
  "qspi_load_ramdisk=sf read ${ramdisk_addr_r} 0x00a00000 0x01580000\0"                                                                \
  "kernel_start_noramdisk=bootm ${kernel_addr_r} - ${fdt_addr_r}\0"                                                                    \
  "kernel_start_ramdisk=bootm ${kernel_addr_r} ${ramdisk_addr_r} ${fdt_addr_r}\0"                                                      \
  "boot_mmc0=echo DAMC-FMC1Z7IO SD boot script && run sd_load_dtb_uimg && setenv bootargs root=/dev/mmcblk0p2 ${bootargs_common} && run kernel_start_noramdisk\0"            \
  "boot_qspi=echo DAMC-FMC1Z7IO eMMC boot script && run emmc_load_dtb_uimg && setenv bootargs root=/dev/mmcblk1p2 ${bootargs_common} && run kernel_start_noramdisk\0"            \
  "boot_net=echo DAMC-FMC1Z7IO QSPI/NFS boot script && run qspi_load_dtb_uimg && setenv bootargs root=/dev/nfs nfsroot=${nfsserver}:${nfsroot},nfsvers=3 ip=dhcp ${bootargs_common} && run kernel_start_noramdisk\0" \
  "boot_recovery=echo DAMC-FMC1Z7IO QSPI/initramfs boot script && run qspi_load_dtb_uimg && run qspi_load_ramdisk && setenv bootargs root=/dev/ram0 ${bootargs_common} && run kernel_start_ramdisk\0" \
  "nfsserver=192.168.1.92\0"            \
  "nfsroot=/nfsroot/z7io\0"             \
  "boot_targets=recovery\0"             \
  "distro_bootcmd=for target in ${boot_targets}; do run boot_${target}; done\0" \
