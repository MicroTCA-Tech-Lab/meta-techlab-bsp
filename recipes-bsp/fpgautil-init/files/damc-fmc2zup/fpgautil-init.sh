#!/bin/sh

scriptname="fpgautil-init"

get_chip_variant() {

    chip_idcode=$(dd if=/sys/bus/nvmem/devices/zynqmp-nvmem0/nvmem bs=4 count=1 skip=1 status=none | od -t x4 | cut -d' ' -f2 | head -n1)
    case ${chip_idcode} in

    "04740093")
        chip_variant="zu11eg"
        ;;

    "14758093")
        chip_variant="zu19eg"
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
fpgautil -b /lib/firmware/base/${chip_variant}/damc_fmc2zup_top.bit.bin -o /lib/firmware/base/${chip_variant}/base.dtbo
echo "${scriptname}: FPGA image download done"
