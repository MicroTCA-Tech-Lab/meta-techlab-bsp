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

#pragma once

#include "fpga_mailbox_layout.h"

bool mb_get_mmc_information(mb_mmc_information_t* info);
bool mb_get_mmc_sensors(mb_mmc_sensor_t* sen, size_t first_sensor, size_t n);
bool mb_get_fru_description(mb_fru_description_t* desc, size_t fru_id);
bool mb_get_fru_status(mb_fru_status_t* stat, size_t fru_id);
bool mb_get_fpga_ctrl(mb_fpga_ctrl_t* ctrl);
