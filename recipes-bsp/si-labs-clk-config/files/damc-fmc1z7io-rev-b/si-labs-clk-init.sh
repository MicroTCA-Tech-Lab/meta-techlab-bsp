get_board_rev() {
    # PS-MIO0 is Rev.C detect. It is low (0) if we're on Rev.C
    echo 906 > /sys/class/gpio/export
    REVC_DETECT=$(cat /sys/class/gpio/gpio906/value)

    case ${REVC_DETECT} in

    "1")
        BOARD_REV="revB"
        ;;

    "0")
        BOARD_REV="revC"
        ;;

    esac

    echo "${0}: Detected board '${BOARD_REV}'"
}

get_board_rev

echo "$0: configuring clocks"

si-labs-clk-config.py 0x75 /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_${BOARD_REV}_0x75_mgtpll_out1_156_25_out2_156_25.txt 2>&1
si-labs-clk-config.py 0x76 /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_${BOARD_REV}_0x76_mainpll_out1_200_00_out2_156_25.txt 2>&1
si-labs-clk-config.py 0x77 /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_${BOARD_REV}_0x77_rtmpll_out1_200_00_out2_200_00.txt 2>&1

echo "$0: clock config done"
