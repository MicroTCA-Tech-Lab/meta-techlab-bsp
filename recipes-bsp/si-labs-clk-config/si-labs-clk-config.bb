COMPATIBLE_MACHINE = "damc-fmc1z7io|damc-fmc2zup"

DESCRIPTION = "Configuration tool for Si Labs chips on I2C bus"
LICENSE = "CLOSED"
PV = "1.3"
PR = "r0"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

S = "${WORKDIR}"

SRC_URI = " \
    file://setup.py \
    file://si-labs-clk-config.py \
    file://slcc/BoardConfig.py \
    file://slcc/extra_logging.py \
    file://slcc/Si534xdriver.py \
    file://slcc/SiLabsTxtParser.py \
    file://si-labs-clk-init.sh \
"

SRC_URI_append_damc-fmc2zup = " \
    file://example_config/example_zup_0x75_zone3.txt \
    file://example_config/example_zup_0x76_ps.txt \
    file://example_config/example_zup_0x77_zup.txt \
"

SRC_URI_append_damc-fmc1z7io-rev-a = " \
    file://example_config/z7io_0x75_out1_125_00_out2_125_00.txt \
    file://example_config/z7io_0x75_out1_156_25_out2_156_25.txt \
    file://example_config/z7io_0x77_out1_200_00_out2_200_00.txt \
"

SRC_URI_append_damc-fmc1z7io-rev-b = " \
    file://example_config/z7io_revB_0x75_mgtpll_out1_156_25_out2_156_25.txt \
    file://example_config/z7io_revB_0x76_mainpll_out1_200_00_out2_156_25.txt \
    file://example_config/z7io_revB_0x77_rtmpll_out1_200_00_out2_200_00.txt \
"

RDEPENDS_${PN} = "python3 python3-smbus i2c-bus-locator"

inherit setuptools3

SLCC_BASE_DIR = "${TECHLAB_BOARD_DIR}/clock_config"

FILES_${PN}_append_damc-fmc2zup = " \
    ${SLCC_BASE_DIR}/0x75_zone3.txt \
    ${SLCC_BASE_DIR}/0x76_ps.txt \
    ${SLCC_BASE_DIR}/0x77_zup.txt \
    ${SLCC_BASE_DIR}/example_zup_0x75_zone3.txt \
    ${SLCC_BASE_DIR}/example_zup_0x76_ps.txt \
    ${SLCC_BASE_DIR}/example_zup_0x77_zup.txt \
"

FILES_${PN}_append_damc-fmc1z7io-rev-a = " \
    ${SLCC_BASE_DIR}/0x75_mgt_125_00.txt \
    ${SLCC_BASE_DIR}/0x75_mgt_156_25.txt \
    ${SLCC_BASE_DIR}/0x77_rtm.txt \
    ${SLCC_BASE_DIR}/z7io_0x75_out1_125_00_out2_125_00.txt \
    ${SLCC_BASE_DIR}/z7io_0x75_out1_156_25_out2_156_25.txt \
    ${SLCC_BASE_DIR}/z7io_0x77_out1_200_00_out2_200_00.txt \
"

FILES_${PN}_append_damc-fmc1z7io-rev-b = " \
    ${SLCC_BASE_DIR}/0x75_mgt_pll.txt \
    ${SLCC_BASE_DIR}/0x76_main_pll.txt \
    ${SLCC_BASE_DIR}/0x77_rtm_pll.txt \
    ${SLCC_BASE_DIR}/z7io_revB_0x75_mgtpll_out1_156_25_out2_156_25.txt \
    ${SLCC_BASE_DIR}/z7io_revB_0x76_mainpll_out1_200_00_out2_156_25.txt \
    ${SLCC_BASE_DIR}/z7io_revB_0x77_rtmpll_out1_200_00_out2_200_00.txt \
"

do_install_append_damc-fmc2zup() {
    SLCC_INSTALL_DIR=${D}${base_prefix}${SLCC_BASE_DIR}
    install -d ${SLCC_INSTALL_DIR}
    install -m 0644 ${S}/example_config/example_zup_0x75_zone3.txt ${SLCC_INSTALL_DIR}
    install -m 0644 ${S}/example_config/example_zup_0x76_ps.txt    ${SLCC_INSTALL_DIR}
    install -m 0644 ${S}/example_config/example_zup_0x77_zup.txt   ${SLCC_INSTALL_DIR}

    # configs are symbolic links so that other applications can overwrite them
    ln -s example_zup_0x75_zone3.txt ${SLCC_INSTALL_DIR}/0x75_zone3.txt
    ln -s example_zup_0x76_ps.txt    ${SLCC_INSTALL_DIR}/0x76_ps.txt
    ln -s example_zup_0x77_zup.txt   ${SLCC_INSTALL_DIR}/0x77_zup.txt
}

do_install_append_damc-fmc1z7io-rev-a() {
    SLCC_INSTALL_DIR=${D}${base_prefix}${SLCC_BASE_DIR}
    install -d ${SLCC_INSTALL_DIR}
    install -m 0644 ${S}/example_config/z7io_0x75_out1_125_00_out2_125_00.txt  ${SLCC_INSTALL_DIR}
    install -m 0644 ${S}/example_config/z7io_0x75_out1_156_25_out2_156_25.txt  ${SLCC_INSTALL_DIR}
    install -m 0644 ${S}/example_config/z7io_0x77_out1_200_00_out2_200_00.txt  ${SLCC_INSTALL_DIR}

    # configs are symbolic links so that other applications can overwrite them
    ln -s z7io_0x75_out1_125_00_out2_125_00.txt  ${SLCC_INSTALL_DIR}/0x75_mgt_125_00.txt
    ln -s z7io_0x75_out1_156_25_out2_156_25.txt ${SLCC_INSTALL_DIR}/0x75_mgt_156_25.txt
    ln -s z7io_0x77_out1_200_00_out2_200_00.txt  ${SLCC_INSTALL_DIR}/0x77_rtm.txt
}

do_install_append_damc-fmc1z7io-rev-b() {
    SLCC_INSTALL_DIR=${D}${base_prefix}${SLCC_BASE_DIR}
    install -d ${SLCC_INSTALL_DIR}
    install -m 0644 ${S}/example_config/z7io_revB_0x75_mgtpll_out1_156_25_out2_156_25.txt  ${SLCC_INSTALL_DIR}
    install -m 0644 ${S}/example_config/z7io_revB_0x76_mainpll_out1_200_00_out2_156_25.txt ${SLCC_INSTALL_DIR}
    install -m 0644 ${S}/example_config/z7io_revB_0x77_rtmpll_out1_200_00_out2_200_00.txt  ${SLCC_INSTALL_DIR}

    # configs are symbolic links so that other applications can overwrite them
    ln -s z7io_revB_0x75_mgtpll_out1_156_25_out2_156_25.txt  ${SLCC_INSTALL_DIR}/0x75_mgt_pll.txt
    ln -s z7io_revB_0x76_mainpll_out1_200_00_out2_156_25.txt ${SLCC_INSTALL_DIR}/0x76_main_pll.txt
    ln -s z7io_revB_0x77_rtmpll_out1_200_00_out2_200_00.txt  ${SLCC_INSTALL_DIR}/0x77_rtm_pll.txt
}

do_install_append() {
    # init script to program the clocks at the startup
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d
    install -m 0755 ${S}/si-labs-clk-init.sh  ${D}${sysconfdir}/init.d/

    ln -sf ../init.d/si-labs-clk-init.sh ${D}${sysconfdir}/rcS.d/S80si-labs-clk-init
}
