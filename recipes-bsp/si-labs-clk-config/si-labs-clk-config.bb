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

SRC_URI_append_damc-fmc1z7io = " \
    file://example_config/z7io_revB_0x75_mgtpll_out1_156_25_out2_156_25.txt \
    file://example_config/z7io_revB_0x76_mainpll_out1_200_00_out2_156_25.txt \
    file://example_config/z7io_revB_0x77_rtmpll_out1_200_00_out2_200_00.txt \
"

RDEPENDS_${PN} = "python3 python3-smbus i2c-bus-locator"

inherit setuptools3

FILES_${PN}_append_damc-fmc2zup = " \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x75_zone3.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x76_ps.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x77_zup.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/example_zup_0x75_zone3.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/example_zup_0x76_ps.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/example_zup_0x77_zup.txt \
"

FILES_${PN}_append_damc-fmc1z7io = " \
    /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/0x75_mgt_pll.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/0x76_main_pll.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/0x77_rtm_pll.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_revB_0x75_mgtpll_out1_156_25_out2_156_25.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_revB_0x76_mainpll_out1_200_00_out2_156_25.txt \
    /opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_revB_0x77_rtmpll_out1_200_00_out2_200_00.txt \
"

do_install_append_damc-fmc2zup() {
    install -d ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/
    install -m 0644 ${WORKDIR}/example_config/example_zup_0x75_zone3.txt  ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/
    install -m 0644 ${WORKDIR}/example_config/example_zup_0x76_ps.txt  ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/
    install -m 0644 ${WORKDIR}/example_config/example_zup_0x77_zup.txt ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/

    # configs are symbolic links so that other applications can overwrite them
    ln -s -r ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/example_zup_0x75_zone3.txt \
        ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x75_zone3.txt
    ln -s -r ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/example_zup_0x76_ps.txt \
        ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x76_ps.txt
    ln -s -r ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/example_zup_0x77_zup.txt \
        ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x77_zup.txt

}

do_install_append_damc-fmc1z7io() {
    install -d ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/
    install -m 0644 ${WORKDIR}/example_config/z7io_revB_0x75_mgtpll_out1_156_25_out2_156_25.txt ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/
    install -m 0644 ${WORKDIR}/example_config/z7io_revB_0x76_mainpll_out1_200_00_out2_156_25.txt ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/
    install -m 0644 ${WORKDIR}/example_config/z7io_revB_0x77_rtmpll_out1_200_00_out2_200_00.txt ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/

    # configs are symbolic links so that other applications can overwrite them
    ln -s -r ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_revB_0x75_mgtpll_out1_156_25_out2_156_25.txt \
        ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/0x75_mgt_pll.txt
    ln -s -r ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_revB_0x76_mainpll_out1_200_00_out2_156_25.txt \
        ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/0x76_main_pll.txt
    ln -s -r ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/z7io_revB_0x77_rtmpll_out1_200_00_out2_200_00.txt \
        ${D}${base_prefix}/opt/mtca-tech-lab/damc-fmc1z7io/clock_config/0x77_rtm_pll.txt
}

do_install_append() {
    # init script to program the clocks at the startup
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d
    install -m 0755 ${WORKDIR}/si-labs-clk-init.sh  ${D}${sysconfdir}/init.d/

    ln -sf ../init.d/si-labs-clk-init.sh ${D}${sysconfdir}/rcS.d/S80si-labs-clk-init
}
