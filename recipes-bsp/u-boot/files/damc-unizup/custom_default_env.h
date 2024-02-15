// clang-format off
//
// We should upgrade to text-based environment some time.
// Current u-boot version (Petalinux 2020.2) doesn't seem to support it yet

#undef CONFIG_EXTRA_ENV_SETTINGS
#define CONFIG_EXTRA_ENV_SETTINGS       \
	/* "board" and "board_name" already used (zynq/zynqmp) */ \
	"amc_name=damc-unizup\0"        \
	/* Addresses & sizes */		\
	"fdt_high=10000000\0"           \
	"fdt_addr_r=0x40000000\0"       \
	"fdt_size_r=0x00040000\0"       \
	"kernel_addr_r=0x18000000\0"    \
	"kernel_size_r=0x02000000\0"    \
	"ramdisk_addr_r=0x02100000\0"   \
	"ramdisk_size_r=0x05D80000\0"   \
	"script_size_f=0x80000\0"       \
	"scriptaddr=0x20000000\0"       \
	/* Load kernel & dtb into memory */                                                                                                            \
	"sd_load_dtb_img=fatload mmc 1 ${fdt_addr_r} ${amc_name}-system.dtb && fatload mmc 1 ${kernel_addr_r} Image\0"                                 \
	"emmc_load_dtb_img=fatload mmc 0 ${fdt_addr_r} ${amc_name}-system.dtb && fatload mmc 0 ${kernel_addr_r} Image\0"                               \
	"qspi_load_dtb_img=sf probe 0 0 0 && sf read ${fdt_addr_r} 0x00240000 ${fdt_size_r} && sf read ${kernel_addr_r} 0x00280000 ${kernel_size_r}\0" \
	"nfs_load_dtb_img=dhcp && nfs ${fdt_addr_r} ${nfsserver}:${nfsroot}/boot/${amc_name}-system.dtb && nfs ${kernel_addr_r} ${nfsserver}:${nfsroot}/boot/Image\0" \
	"tftp_load_dtb_img=dhcp && tftpboot ${fdt_addr_r} ${tftpserver}:${amc_name}-system.dtb && tftpboot ${kernel_addr_r} ${tftpserver}:Image\0"     \
	/* Load ramdisk into memory */                                                                                                                 \
	"qspi_load_ramdisk=sf read ${ramdisk_addr_r} 0x02280000 ${ramdisk_size_r}\0"                                                                   \
	"nfs_load_ramdisk=run set_ramdisk_name && nfs ${ramdisk_addr_r} ${nfsserver}:${nfsroot}/boot/${ramdisk_name}\0"                                \
	"tftp_load_ramdisk=run set_ramdisk_name && tftpboot ${ramdisk_addr_r} ${tftpserver}:${ramdisk_name}\0"                                         \
	/* Bootargs */                                                                                                                                 \
	"bootargs_common='earlycon clk_ignore_unused rw rootwait cpuidle.off=1 uio_pdrv_genirq.of_id=\"generic-uio\" video=DP-1'\0"                    \
	"set_bootargs_ramdisk=setenv bootargs root=/dev/ram0 ${bootargs_common}\0"                                                                     \
	"set_bootargs_nfsroot=setenv bootargs root=/dev/nfs nfsroot=${nfsserver}:${nfsroot},nfsvers=3 ip=dhcp ${bootargs_common}\0"                    \
	/* Start linux without ramdisk */                                                                                                              \
	"kernel_start_noramdisk=booti ${kernel_addr_r} - ${fdt_addr_r}\0"                                                                              \
	/* Start linux with ramdisk */                                                                                                                 \
	"kernel_start_ramdisk=booti ${kernel_addr_r} ${ramdisk_addr_r} ${fdt_addr_r}\0"                                                                \
	/* Boot scripts */                                                                                                                             \
	"boot_mmc0=echo ${amc_name} eMMC boot script            && run emmc_load_dtb_img && setenv bootargs root=/dev/mmcblk0p2 ${bootargs_common} && run kernel_start_noramdisk\0" \
	"boot_mmc1=echo ${amc_name} SD boot script              && run sd_load_dtb_img   && setenv bootargs root=/dev/mmcblk1p2 ${bootargs_common} && run kernel_start_noramdisk\0" \
	"boot_qspi_nfs=echo ${amc_name} QSPI/NFS boot script    && run qspi_load_dtb_img && run set_bootargs_nfsroot && run kernel_start_noramdisk\0"                               \
	"boot_qspi0=echo ${amc_name} QSPI/ramdisk boot script   && run qspi_load_dtb_img && run qspi_load_ramdisk && run set_bootargs_ramdisk && run kernel_start_ramdisk\0"        \
	"boot_nfs=echo ${amc_name} NFS boot script              && run nfs_load_dtb_img  && run set_bootargs_nfsroot && run kernel_start_noramdisk\0"                               \
	"boot_nfs_ramdisk=echo ${amc_name} NFS/ramdisk boot script && run nfs_load_dtb_img && run nfs_load_ramdisk && run set_bootargs_ramdisk && run kernel_start_ramdisk\0"       \
	"boot_tftp_ramdisk=echo ${amc_name} TFTP/ramdisk boot script && run tftp_load_dtb_img && run tftp_load_ramdisk && run set_bootargs_ramdisk && run kernel_start_ramdisk\0"   \
	/* Make sure that dhcp only gets an address for us, nothing else */                           \
	"autoload=no\0"                                                                               \
	"tftpserver=192.168.1.92\0"                                                                   \
	"nfsserver=192.168.1.92\0"                                                                    \
	"nfsroot=/nfsroot/unizup\0"                                                                   \
	"set_ramdisk_name=setenv ramdisk_name techlab-recovery-${amc_name}.cpio.gz.u-boot\0"          \
	"distro_bootcmd=for target in ${boot_targets}; do run boot_${target}; done; run boot_qspi0\0" \

