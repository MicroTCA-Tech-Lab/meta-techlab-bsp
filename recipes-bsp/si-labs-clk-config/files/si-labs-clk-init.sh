
echo "$0: configuring clocks"

si-labs-clk-config.py 0x77 /opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x77_zup.txt 2>&1
# 0x77 is the main PLL, and it should be configured before Zone 3 PLL at 0x75
si-labs-clk-config.py 0x75 /opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x75_zup.txt 2>&1

echo "$0: clock config done"

