
echo "$0: configuring clocks"

si-labs-clk-config.py 0x76 /opt/mtca-tech-lab/damc-motctrl/clock_config/0x76_mainpll.txt 2>&1

echo "$0: clock config done"