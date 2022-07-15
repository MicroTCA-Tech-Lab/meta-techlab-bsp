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

#include "mmcmb/fpga_mailbox_layout.h"

#ifndef MB_DEVICE_FILE
#error "No mailbox file path provided!"
#endif

static int fd = -1;

static bool mb_open(void)
{
    if (fd < 0) {
        fd = open(MB_DEVICE_FILE, O_RDWR);
    }
    if (fd < 0) {
        perror("could not open " MB_DEVICE_FILE);
        return false;
    }
    return true;
}

static bool mb_read_at(size_t offs, void* buf, size_t n)
{
    if (!mb_open()) {
        return false;
    }

    ssize_t n_read = pread(fd, buf, n, offs);
    if (n_read != n) {
        perror("read error");
        return false;
    }
    return true;
}

bool mb_get_mmc_information(mb_mmc_information_t* info)
{
    return mb_read_at(MB_EEPROM_OFFS(mmc_information), info, sizeof(mb_mmc_information_t));
}

bool mb_get_mmc_sensors(mb_mmc_sensor_t* sen, size_t first_sensor, size_t n)
{
    if (first_sensor + n > MAX_SENS_MMC) {
        fprintf(stderr, "Sensor index out of range (%u > %u)\n", first_sensor + n, MAX_SENS_MMC);
        return false;
    }
    return mb_read_at(MB_EEPROM_OFFS(mmc_sensor[first_sensor]), sen, sizeof(mb_mmc_sensor_t) * n);
}

bool mb_get_fru_description(mb_fru_description_t* desc, size_t fru_id)
{
    if (fru_id >= NUM_FRUS) {
        fprintf(stderr, "FRU index out of range (%u >= %u)\n", fru_id, NUM_FRUS);
        return false;
    }
    return mb_read_at(MB_EEPROM_OFFS(fru_information[fru_id].description),
                      desc,
                      sizeof(mb_fru_description_t));
}

bool mb_get_fru_status(mb_fru_status_t* stat, size_t fru_id)
{
    if (fru_id >= NUM_FRUS) {
        fprintf(stderr, "FRU index out of range (%u >= %u)\n", fru_id, NUM_FRUS);
        return false;
    }
    return mb_read_at(MB_EEPROM_OFFS(fru_information[fru_id].status),
                      stat,
                      sizeof(mb_fru_status_t));
}

bool mb_get_fpga_ctrl(mb_fpga_ctrl_t* ctrl)
{
    return mb_read_at(MB_EEPROM_OFFS(fpga_ctrl), ctrl, sizeof(mb_fpga_ctrl_t));
}
