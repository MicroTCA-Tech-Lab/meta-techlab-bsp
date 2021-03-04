#! /bin/sh

#set -x

SCRIPT_NAME=$0

# 172 = pl_reset1
# see https://forums.xilinx.com/t5/Embedded-Linux/GPIO-control-in-Linux-sysfs/td-p/833075
# and https://www.xilinx.com/support/answers/68962.html

PL_RESET_OFFSET=172
# reset level: 0 = active high, 1 = active low
RESET_LEVEL=1

#===============================================================================
# find GPIO controller

for ctrl in /sys/class/gpio/gpiochip*; do
    ctrl_label=$(cat ${ctrl}/label);

    if [ "${ctrl_label}" = "zynqmp_gpio" ]; then
        echo "$SCRIPT_NAME: found zynqmp gpio at $ctrl"
        zynq_ctrl=$ctrl;
    fi;

done

if [ -z "$zynq_ctrl" ]; then
    echo "$SCRIPT_NAME: zynqmp gpio was not found, exiting"
    exit 1;
fi

#===============================================================================
# find GPIO offset

ctrl_base=$(cat ${zynq_ctrl}/base)
echo "$SCRIPT_NAME: zynqmp gpio base at ${ctrl_base}"

pl_reset_gpio=$((${ctrl_base} + ${PL_RESET_OFFSET}))
echo "$SCRIPT_NAME: reset gpio at offset ${pl_reset_gpio}"

#===============================================================================
# export GPIO (if not yet)

gpio_dir="/sys/class/gpio/gpio${pl_reset_gpio}"

if [ ! -d $gpio_dir ]; then
    echo "$SCRIPT_NAME: writing to gpio export"
    echo ${pl_reset_gpio} > /sys/class/gpio/export
else
    echo "$SCRIPT_NAME: gpio dir already exist, skipping export"
fi;


#===============================================================================
# drive GPIO to '0' for 1s, then leave it at '1'

LEVEL_ASSERT=$((1-${RESET_LEVEL}))
LEVEL_DEASSERT=${RESET_LEVEL}

echo "$SCRIPT_NAME: driving gpio pin to '$LEVEL_ASSERT' - reset asserted"
echo ${LEVEL_ASSERT} > ${gpio_dir}/value

sleep 1

echo "$SCRIPT_NAME: driving gpio pin to '$LEVEL_DEASSERT' - reset deasserted"
echo ${LEVEL_DEASSERT} > ${gpio_dir}/value

