CRIPTION = "Configuration tool for Si Labs chips on I2C bus"
LICENSE = "CLOSED"
PV = "1.2"
PR = "r1"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

S = "${WORKDIR}"

SRC_URI = " \
    file://setup.py \
    file://si-labs-clk-config.py \
    file://slcc/extra_logging.py \
    file://slcc/Si534xdriver.py \
    file://slcc/SiLabsTxtParser.py \
    file://example_config/example_zup_0x75_zone3.txt \
    file://example_config/example_zup_0x76_ps.txt \
    file://example_config/example_zup_0x77_zup.txt \
    file://si-labs-clk-init.sh \
"

RDEPENDS_${PN} = "python python3-smbus"

inherit setuptools3

FILES_${PN} += " \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x75_zone3.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x76_ps.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/0x77_zup.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/example_zup_0x75_zone3.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/example_zup_0x76_ps.txt \
    /opt/mtca-tech-lab/damc-fmc2zup/clock_config/example_zup_0x77_zup.txt \
"

do_install_append() {
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

    # init script to program the clocks at the startup
    install -d ${D}${sysconfdir}/init.d
    install -d ${D}${sysconfdir}/rcS.d

    install -m 0755 ${WORKDIR}/si-labs-clk-init.sh  ${D}${sysconfdir}/init.d/

    ln -sf ../init.d/si-labs-clk-init.sh ${D}${sysconfdir}/rcS.d/S80si-labs-clk-init
}
