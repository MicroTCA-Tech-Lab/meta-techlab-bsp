do_install_append () {
    sed -i -e 's:#Banner none:Banner /etc/banner:' ${D}${sysconfdir}/ssh/sshd_config
}