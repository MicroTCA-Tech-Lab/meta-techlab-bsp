
# cpuidle.off=1  -->  https://www.xilinx.com/support/answers/69143.html
#
# uio_pdrv_genirq.of_id="generic-uio" -->
#    https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18842482/Device+Tree+Tips#DeviceTreeTips-8.1KernelBootargs

KERNEL_BOOTARGS_zynqmp_append = 'cpuidle.off=1 uio_pdrv_genirq.of_id="generic-uio"'

