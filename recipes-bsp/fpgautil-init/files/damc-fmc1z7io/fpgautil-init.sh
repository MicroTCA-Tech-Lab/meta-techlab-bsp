#!/bin/sh

scriptname="fpgautil-init"

get_chip_variant() {

    chip_idcode=$(cat /sys/devices/soc0/soc_id)
    case ${chip_idcode} in

    "0xc")
        chip_variant="7z030"
        ;;

    "0x0c")
        chip_variant="7z030"
        ;;

    "0x12")
        chip_variant="7z035"
        ;;

    "0x11")
        chip_variant="7z045"
        ;;

    *)
        echo "${scriptname}: Chip variant not found: unknown ID code of '${chip_idcode}'"
        echo "${scriptname}: FPGA configuration aborted"
        exit 1
        ;;
    esac

    echo "${scriptname}: Detected FPGA chip variant '${chip_variant}'"
}

get_chip_variant

echo "${scriptname}: Downloading FPGA image"
fpgautil -b /lib/firmware/xilinx/base/${chip_variant}/damc_fmc1z7io_top.bit.bin -o /lib/firmware/xilinx/base/${chip_variant}/base.dtbo
echo "${scriptname}: FPGA image download done"
