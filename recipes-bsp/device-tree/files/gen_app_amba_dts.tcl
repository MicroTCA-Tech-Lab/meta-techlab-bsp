
# Copyright (c) 2021 Deutsches Elektronen-Synchrotron DESY

# creates dts_app/zup_app.dts


if {$argc != 3} {
	puts "Usage: $argv0 XSCT_DIR WORKDIR"
	exit 1
}

set XSCT_DIR [lindex $argv 0]
set WORKDIR [lindex $argv 1]
set HDF_OR_XSA_PATH [lindex $argv 2]

puts "XSCT_DIR: $XSCT_DIR"
puts "WORKDIR: $WORKDIR"
puts "HDF_OR_XSA_PATH: $HDF_OR_XSA_PATH"


source ${XSCT_DIR}/scripts/hsm/xillib_hw.tcl
source ${XSCT_DIR}/scripts/hsm/xillib_sw.tcl

hsi::set_repo_path $WORKDIR/git
hsi::open_hw_design $HDF_OR_XSA_PATH

set tree [hsi::create_dt_tree -dts_file zup_app.dts]
set root_node [hsi::create_dt_node -name "/"]
set bus_node [hsi::create_dt_node -name "amba_app" -label "amba_app" -unit_addr 0 -object $root_node]

hsi::utils::add_new_dts_param $bus_node "#address-cells" "2" comment
hsi::utils::add_new_dts_param $bus_node "#size-cells" "2" comment
hsi::utils::add_new_dts_param $bus_node "compatible" "simple-bus" string
hsi::utils::add_new_dts_param $bus_node "ranges" "" boolean


foreach cell [hsi::get_cells] {
    set comp_name [hsi::get_property CONFIG.Component_Name [hsi::get_cells $cell]]
    set is_in_app [string match "system_app*" $comp_name]
    # puts "$is_in_app : $cell"

    if {$is_in_app} {
        set mem_ranges [hsi::get_mem_ranges [hsi::get_cells $cell]]

        set mem ""
        foreach mem_range $mem_ranges {
            set mst_iface [hsi::get_property MASTER_INTERFACE $mem_range]
            if {[string match "arm_lpd_m_axi" $mst_iface]} {
                # puts "  $mst_iface"
                set mem $mem_range
            }
        }

        if {[expr {$mem ne ""}]} {

            set base [string tolower [hsi::get_property BASE_VALUE $mem]]
            set high [string tolower [hsi::get_property HIGH_VALUE $mem]]
            set size [format 0x%x [expr {${high} - ${base} + 1}]]

            if {[regexp -nocase {0x([0-9a-f]{9})} "$base" match]} {
                set temp $base
                set temp [string trimleft [string trimleft $temp 0] x]
                set len [string length $temp]
                set rem [expr {${len} - 8}]
                set high_base "0x[string range $temp $rem $len]"
                set low_base "0x[string range $temp 0 [expr {${rem} - 1}]]"
                set low_base [format 0x%08x $low_base]
                if {[regexp -nocase {0x([0-9a-f]{9})} "$size" match]} {
                    set temp $size
                    set temp [string trimleft [string trimleft $temp 0] x]
                    set len [string length $temp]
                    set rem [expr {${len} - 8}]
                    set high_size "0x[string range $temp $rem $len]"
                    set low_size  "0x[string range $temp 0 [expr {${rem} - 1}]]"
                    set low_size [format 0x%08x $low_size]
                    set reg "$low_base $high_base $low_size $high_size"
                } else {
                    set reg "$low_base $high_base 0x0 $size"
                }
            } else {
                set reg "0x0 $base 0x0 $size"
            }

            set ip_name [hsi::get_property HIER_NAME [hsi::get_cells $cell]]
	    set unit_addr [string range $base 2 99]
            set comp_node [hsi::create_dt_node -name $ip_name -label $ip_name -unit_addr $unit_addr -object $bus_node]
            hsi::utils::add_new_dts_param $comp_node "compatible" "generic-uio" string
            hsi::utils::add_new_dts_param $comp_node "reg" "$reg" intlist
        }
    }
}


hsi::create_sw_design dt1 -os device_tree -proc psu_cortexa53_0
hsi::generate_target -dir dts_app

