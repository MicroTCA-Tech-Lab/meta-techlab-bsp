
echo "$0: configuring clocks"

si-labs-clk-config.py 0x75 /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_revB_0x75_mgtpll_out1_156_25_out2_156_25.txt 2>&1
si-labs-clk-config.py 0x76 /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_revB_0x76_mainpll_out1_200_00_out2_156_25.txt 2>&1
si-labs-clk-config.py 0x77 /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_revB_0x77_rtmpll_out1_200_00_out2_200_00.txt 2>&1

echo "$0: clock config done"
