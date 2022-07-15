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

#include <stdint.h>

#define MB_PACKED __attribute__((packed)) __attribute__((scalar_storage_order("little-endian")))

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#pragma GCC diagnostic ignored "-Wpacked"

/* FPGA Mailbox data types */

typedef struct mb_fru_status {
    unsigned present : 1;
    unsigned compatible : 1;
    unsigned powered : 1;
    unsigned failure : 1;
    unsigned status_reserved : 4;
    uint8_t num_temp_sensors;
    uint16_t temperature[4];
    uint8_t bytes_reserved[10];
} MB_PACKED mb_fru_status_t;

typedef struct mb_fru_description {
    uint8_t uid[6];
    char manufacturer[60];
    char product[60];
    char part_nr[60];
    char serial_nr[30];
    char version[20];
} MB_PACKED mb_fru_description_t;

typedef struct mb_fru_information {
    mb_fru_status_t status;
    mb_fru_description_t description;
} MB_PACKED mb_fru_information_t;

typedef struct mb_version_number {
    uint8_t major;
    uint8_t minor;
} MB_PACKED mb_version_number_t;

typedef struct mb_mmc_information {
    mb_version_number_t application_version;
    mb_version_number_t library_version;
    mb_version_number_t cpld_version;
    char stamp_hw_revision;
    uint8_t amc_slot_nr;
    uint8_t ipmb_addr;
    char board_name[23];
    uint16_t vendor_id;
    uint16_t product_id;
    uint32_t mmc_uptime;
    uint8_t reserved[8];
} MB_PACKED mb_mmc_information_t;

typedef struct mb_mmc_sensor {
    char name[12];
    float reading;
} MB_PACKED mb_mmc_sensor_t;

typedef struct mb_fpga_ctrl {
    unsigned req_shutdown : 1;
    unsigned req_pcie_reset : 1;
    unsigned reserved : 6;
} MB_PACKED mb_fpga_ctrl_t;

typedef struct mb_fpga_status {
    unsigned app_startup_finished : 1;
    unsigned app_failure : 1;
    unsigned app_shutdown_finished : 1;
    unsigned reserved : 5;
} MB_PACKED mb_fpga_status_t;

/* Full memory content, containing the sub-types */

typedef struct mb_memory_contents {
    mb_fru_information_t fru_information[4];
    uint8_t application_data[256];
    mb_mmc_information_t mmc_information;
    mb_mmc_sensor_t mmc_sensor[40];
    uint8_t reserved[77];
    mb_fpga_ctrl_t fpga_ctrl;
    mb_fpga_status_t fpga_status;
} MB_PACKED mb_memory_contents_t;

#pragma GCC diagnostic pop

/* Convenience macros */

/* EEPROM offset of a data structure field */
#define MB_MEM_DUMMY ((const mb_memory_contents_t*)NULL)
#define MB_EEPROM_OFFS(x) (uintptr_t)(&MB_MEM_DUMMY->x)

/* Array sizes */
#define MB_NUM_ELEMS(x) (sizeof(MB_MEM_DUMMY->x) / sizeof(MB_MEM_DUMMY->x[0]))
#define NUM_FRUS MB_NUM_ELEMS(fru_information)
#define MAX_SENS_PER_FRU MB_NUM_ELEMS(fru_information[0].status.temperature)
#define MAX_SENS_MMC MB_NUM_ELEMS(mmc_sensor)
