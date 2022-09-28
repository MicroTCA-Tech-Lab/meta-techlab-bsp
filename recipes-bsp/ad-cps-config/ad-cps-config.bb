COMPATIBLE_MACHINE = "damc-fmc1z7io"

DESCRIPTION = "Configuration tool for AD CPS on I2C bus"
LICENSE = "CLOSED"
PV = "1.3"
PR = "r1"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

S = "${WORKDIR}"

SRC_URI = " \
    file://setup.py \
    file://ad-cps-config.py \
    file://adn/extra_logging.py \
    file://adn/ADN4612driver.py \
    file://adn/ADN4612TxtParser.py \
    file://ad-cps-init.sh \
"

SRC_URI_append_damc-fmc1z7io-rev-a = " \
    file://example_config/z7io_0x44_register_map_fmc2_dp1_dp2.txt \
    file://example_config/z7io_0x44_register_map_llc0_llc1.txt \
    file://example_config/z7io_0x44_register_map_llc2_llc3.txt \
    file://example_config/z7io_0x44_register_map_pcie_x4.txt \
    file://example_config/z7io_0x44_register_map_z3_mgt0_mgt1.txt \
"

SRC_URI_append_damc-fmc1z7io-rev-b = " \
    file://example_config/z7io_0x44_cps_fmc_dp0_dp1.txt \
    file://example_config/z7io_0x44_cps_bp_llc0_llc1.txt \
    file://example_config/z7io_0x44_cps_bp_llc2_llc3.txt \
    file://example_config/z7io_0x44_cps_bp_pcie_x4.txt \
"

RDEPENDS_${PN} = "python3 python3-smbus i2c-bus-locator"

inherit setuptools3

FILES_${PN}_append_damc-fmc1z7io-rev-a = " \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/0x44_fmc2_dp1_dp2.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/0x44_llc0_llc1.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/0x44_llc2_llc3.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/0x44_pcie_x4.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/0x44_z3_mgt0_mgt1.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_register_map_fmc2_dp1_dp2.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_register_map_llc0_llc1.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_register_map_llc2_llc3.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_register_map_pcie_x4.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_register_map_z3_mgt0_mgt1.txt \
"

FILES_${PN}_append_damc-fmc1z7io-rev-b = " \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/0x44_fmc_dp0_dp1.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/0x44_llc0_llc1.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/0x44_llc2_llc3.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/0x44_pcie_x4.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_cps_fmc_dp0_dp1.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_cps_bp_llc0_llc1.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_cps_bp_llc2_llc3.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/cps_config/z7io_0x44_cps_bp_pcie_x4.txt \
"

do_install_append_damc-fmc1z7io-rev-a() {
    CONFDIR="${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/cps_config/"

    install -d ${CONFDIR}
    install -m 0644 ${WORKDIR}/example_config/z7io_0x44_register_map_fmc2_dp1_dp2.txt ${CONFDIR}
    install -m 0644 ${WORKDIR}/example_config/z7io_0x44_register_map_llc0_llc1.txt    ${CONFDIR}
    install -m 0644 ${WORKDIR}/example_config/z7io_0x44_register_map_llc2_llc3.txt    ${CONFDIR}
    install -m 0644 ${WORKDIR}/example_config/z7io_0x44_register_map_pcie_x4.txt      ${CONFDIR}
    install -m 0644 ${WORKDIR}/example_config/z7io_0x44_register_map_z3_mgt0_mgt1.txt ${CONFDIR}

    # configs are symbolic links so that other applications can overwrite them
    ln -s -r ${CONFDIR}/z7io_0x44_register_map_fmc2_dp1_dp2.txt ${CONFDIR}/0x44_fmc2_dp1_dp2.txt
    ln -s -r ${CONFDIR}/z7io_0x44_register_map_llc0_llc1.txt    ${CONFDIR}/0x44_llc0_llc1.txt
    ln -s -r ${CONFDIR}/z7io_0x44_register_map_llc2_llc3.txt    ${CONFDIR}/0x44_llc2_llc3.txt
    ln -s -r ${CONFDIR}/z7io_0x44_register_map_pcie_x4.txt      ${CONFDIR}/0x44_pcie_x4.txt
    ln -s -r ${CONFDIR}/z7io_0x44_register_map_z3_mgt0_mgt1.txt ${CONFDIR}/0x44_z3_mgt0_mgt1.txt
}

do_install_append_damc-fmc1z7io-rev-b() {
    CONFDIR="${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/cps_config/"

    install -d ${CONFDIR}
    install -m 0644 ${WORKDIR}/example_config/z7io_0x44_cps_fmc_dp0_dp1.txt  ${CONFDIR}
    install -m 0644 ${WORKDIR}/example_config/z7io_0x44_cps_bp_llc0_llc1.txt ${CONFDIR}
    install -m 0644 ${WORKDIR}/example_config/z7io_0x44_cps_bp_llc2_llc3.txt ${CONFDIR}
    install -m 0644 ${WORKDIR}/example_config/z7io_0x44_cps_bp_pcie_x4.txt   ${CONFDIR}

    # configs are symbolic links so that other applications can overwrite them
    ln -s -r ${CONFDIR}/z7io_0x44_cps_fmc_dp0_dp1.txt  ${CONFDIR}/0x44_fmc_dp0_dp1.txt
    ln -s -r ${CONFDIR}/z7io_0x44_cps_bp_llc0_llc1.txt ${CONFDIR}/0x44_llc0_llc1.txt
    ln -s -r ${CONFDIR}/z7io_0x44_cps_bp_llc2_llc3.txt ${CONFDIR}/0x44_llc2_llc3.txt
    ln -s -r ${CONFDIR}/z7io_0x44_cps_bp_pcie_x4.txt   ${CONFDIR}/0x44_pcie_x4.txt
}

do_install_append() {
    # init script to program the cps at the startup
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d
    install -m 0755 ${WORKDIR}/ad-cps-init.sh  ${D}${sysconfdir}/init.d/

    ln -sf ../init.d/ad-cps-init.sh ${D}${sysconfdir}/rcS.d/S80ad-cps-init
}