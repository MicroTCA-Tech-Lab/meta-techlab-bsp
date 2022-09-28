
echo "$0: configuring cross-point switch"

ad-cps-config.py 0x44 /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_cps_fmc_dp0_dp1.txt 2>&1
#ad-cps-config.py 0x44 /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_cps_bp_llc0_llc1.txt 2>&1
#ad-cps-config.py 0x44 /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_cps_bp_llc2_llc3.txt 2>&1
#ad-cps-config.py 0x44 /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_cps_bp_pcie_x4.txt 2>&1

echo "$0: cross-point switch config done"
