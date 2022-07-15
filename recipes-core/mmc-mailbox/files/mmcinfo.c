/***************************************************************************
 *      ____  _____________  __    __  __ _           _____ ___   _        *
 *     / __ \/ ____/ ___/\ \/ /   |  \/  (_)__ _ _ __|_   _/ __| /_\  (R)  *
 *    / / / / __/  \__ \  \  /    | |\/| | / _| '_/ _ \| || (__ / _ \      *
 *   / /_/ / /___ ___/ /  / /     |_|  |_|_\__|_| \___/|_| \___/_/ \_\     *
 *  /_____/_____//____/  /_/      T  E  C  H  N  O  L  O  G  Y   L A B     *
 *                                                                         *
 *          Copyright 2022 Deutsches Elektronen-Synchrotron DESY.          *
 *                          All rights reserved.                           *
 *                                                                         *
 ***************************************************************************/

#include <fcntl.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "mmcmb/mmcmb.h"

static char* uptime_format(uint32_t t, char* buf, size_t len)
{
#define SECS_PER_MIN 60
#define MIN_PER_HOUR 60
#define HOURS_PER_DAY 24
    static const struct {
        const char* name;
        uint32_t divisor, modulo;
    } units[] = {
        {"day", HOURS_PER_DAY * MIN_PER_HOUR * SECS_PER_MIN, 0},
        {"hour", MIN_PER_HOUR * SECS_PER_MIN, HOURS_PER_DAY},
        {"minute", SECS_PER_MIN, MIN_PER_HOUR},
        {"second", 1, SECS_PER_MIN},
    };
    *buf = '\0';
    size_t l = 0;
    for (size_t i = 0; i < (sizeof(units) / sizeof(units[0])); i++) {
        unsigned int num = (t / units[i].divisor);
        if (units[i].modulo) {
            num %= units[i].modulo;
        }
        if (l || num) {
            l += snprintf(buf + l,
                          len - l,
                          "%s%d %s%s",
                          l ? ", " : "",
                          num,
                          units[i].name,
                          num == 1 ? "" : "s");
        }
    }
    return buf;
}

static void dump_str(const char* desc, size_t rjust, const char* str, size_t maxlen)
{
    printf("%-*s: %.*s\n", rjust, desc, maxlen, *str ? str : "N/A");
}

static void dump_mmc_information(void)
{
    mb_mmc_information_t info;
    if (!mb_get_mmc_information(&info)) {
        exit(1);
    }

    printf("MMC information\n");
    printf("---------------\n");
    printf("%-16s: %d.%d\n",
           "App version",
           info.application_version.major,
           info.application_version.minor);
    printf("%-16s: %d.%d\n", "Lib version", info.library_version.major, info.library_version.minor);
    printf("%-16s: %d.%d\n", "CPLD version", info.cpld_version.major, info.cpld_version.minor);

    printf("%-16s: Rev. %c\n", "STAMP revision", info.stamp_hw_revision);
    printf("%-16s: %d\n", "AMC slot", info.amc_slot_nr);
    printf("%-16s: 0x%02x\n", "IPMB addr", info.ipmb_addr);
    dump_str("Board name", 16, info.board_name, sizeof(info.board_name));
    printf("%-16s: 0x%04x\n", "IANA Vendor ID", info.vendor_id);
    printf("%-16s: 0x%04x\n", "IANA Product ID", info.product_id);

    char tmp[60];
    printf("%-16s: %s\n", "Uptime", uptime_format(info.mmc_uptime, tmp, sizeof(tmp)));
}

static void dump_mmc_sensors(void)
{
    mb_mmc_sensor_t sen[MAX_SENS_MMC];
    if (!mb_get_mmc_sensors(sen, 0, MAX_SENS_MMC)) {
        exit(1);
    }

    printf("MMC sensors\n");
    printf("-----------\n");
    for (size_t i = 0; i < MAX_SENS_MMC && sen[i].name[0]; i++) {
        printf("%-13.*s: %g\n", sizeof(sen[i].name), sen[i].name, sen[i].reading);
    }
}

static void dump_fru_description(size_t fru_id)
{
    mb_fru_description_t desc;
    if (!mb_get_fru_description(&desc, fru_id)) {
        exit(1);
    }

    printf("FRU %d description\n", fru_id);
    printf("-----------------\n");

    char uid_str[6 * 2 + 1] = "N/A";
    uint8_t uid_zero[sizeof(desc.uid)] = {0};
    if (memcmp(desc.uid, uid_zero, sizeof(desc.uid))) {
        snprintf(uid_str,
                 sizeof(uid_str),
                 "%02X%02X%02X%02X%02X%02X",
                 desc.uid[0],
                 desc.uid[1],
                 desc.uid[2],
                 desc.uid[3],
                 desc.uid[4],
                 desc.uid[5]);
    }
    printf("%-14s: %s\n", "UID", uid_str);
    dump_str("Manufacturer", 14, desc.manufacturer, sizeof(desc.manufacturer));
    dump_str("Product name", 14, desc.product, sizeof(desc.product));
    dump_str("Part number", 14, desc.part_nr, sizeof(desc.part_nr));
    dump_str("Serial number", 14, desc.serial_nr, sizeof(desc.serial_nr));
    dump_str("Version", 14, desc.version, sizeof(desc.version));
}

static void dump_fru_status(size_t fru_id)
{
    mb_fru_status_t stat;
    if (!mb_get_fru_status(&stat, fru_id)) {
        exit(1);
    }

    printf("FRU %d status\n", fru_id);
    printf("-----------------\n");

    printf("%-14s: %cPresent %cCompatible %cPowered %cFailure\n",
           "Flags",
           stat.present ? '+' : '-',
           stat.compatible ? '+' : '-',
           stat.powered ? '+' : '-',
           stat.failure ? '+' : '-');

    for (size_t i = 0; i < stat.num_temp_sensors; i++) {
        printf("Temperature %d : %g C\n", i + 1, (float)stat.temperature[i] / 100.f);
    }
}

int main(int argc, char** argv)
{
    dump_mmc_information();
    printf("\n");
    dump_mmc_sensors();
    printf("\n");

    dump_fru_description(0);
    printf("\n");
    dump_fru_description(1);
    printf("\n");
    dump_fru_description(2);
    printf("\n");

    dump_fru_status(0);
    printf("\n");

    mb_fpga_ctrl_t ctrl;
    if (mb_get_fpga_ctrl(&ctrl)) {
        printf("FPGA Ctrl: %cShdn %cPCIeReset\r\n",
               ctrl.req_shutdown ? '+' : '-',
               ctrl.req_pcie_reset ? '+' : '-');
    }
    return 0;
}
