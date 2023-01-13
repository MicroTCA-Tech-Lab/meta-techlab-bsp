
echo "$0: configuring cross-point switch"

ad-cps-config.py 0x44 /opt/mtca-tech-lab/damc-motctrl/cps_config/motctrl_0x44_cps_eth_sfp.txt 2>&1

echo "$0: cross-point switch config done"
