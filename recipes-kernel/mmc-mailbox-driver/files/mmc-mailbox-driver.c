// SPDX-License-Identifier: GPL-2.0+
/*
 * "Virtual EEPROM" driver for DMMC-STAMP Mailbox
 *
 * Copyright (C) 2022 Patrick Huesmann, DESY
 *
 * Based on at24.c by David Brownell & Wolfram Sang
 *
 */

#include <linux/bitops.h>
#include <linux/delay.h>
#include <linux/gpio/consumer.h>
#include <linux/i2c.h>
#include <linux/init.h>
#include <linux/jiffies.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/mutex.h>
#include <linux/property.h>
#include <linux/regmap.h>
#include <linux/slab.h>

#include <linux/mod_devicetable.h>
#include <linux/nvmem-provider.h>
#include <linux/of_device.h>
#include <linux/pm_runtime.h>

struct at24_data {
    /*
   * Lock protects against activities from other Linux tasks,
   * but not from changes by other I2C masters.
   */
    struct mutex lock;

    unsigned int write_max;

    u32 byte_len;
    u16 page_size;

    struct nvmem_device* nvmem;
    struct i2c_client* client;
    struct regmap* regmap;
};

/*
 * This parameter is to help this driver avoid blocking other drivers out
 * of I2C for potentially troublesome amounts of time. With a 100 kHz I2C
 * clock, one 256 byte read takes about 1/43 second which is excessive;
 * but the 1/170 second it takes at 400 kHz may be quite reasonable; and
 * at 1 MHz (Fm+) a 1/430 second delay could easily be invisible.
 *
 * This value is forced to be a power of two so that writes align on pages.
 */
static unsigned int mmc_mailbox_io_limit = 128;
module_param_named(io_limit, mmc_mailbox_io_limit, uint, 0);
MODULE_PARM_DESC(mmc_mailbox_io_limit, "Maximum bytes per I/O (default 128)");

/*
 * Specs often allow 5 msec for a page write, sometimes 20 msec;
 * it's important to recover from write timeouts.
 */
static unsigned int at24_write_timeout = 25;
module_param_named(write_timeout, at24_write_timeout, uint, 0);
MODULE_PARM_DESC(at24_write_timeout, "Time (in ms) to try writes (default 25)");

struct at24_chip_data {
    u32 byte_len;
};

static const struct at24_chip_data at24_data_dmmc_stamp_mailbox = {
    .byte_len = 16384 / 8,
};

static const struct i2c_device_id mmc_mailbox_ids[] = {
    {"mmcmailbox", (kernel_ulong_t)&at24_data_dmmc_stamp_mailbox},
    {/* END OF LIST */}};

MODULE_DEVICE_TABLE(i2c, mmc_mailbox_ids);

static const struct of_device_id mmc_mailbox_of_match[] = {
    {.compatible = "desy,mmcmailbox", .data = &at24_data_dmmc_stamp_mailbox},
    {/* END OF LIST */},
};
MODULE_DEVICE_TABLE(of, mmc_mailbox_of_match);

static size_t at24_adjust_read_count(struct at24_data* mmc_mailbox,
                                     unsigned int offset,
                                     size_t count)
{
    if (count > mmc_mailbox_io_limit)
        count = mmc_mailbox_io_limit;

    return count;
}

static ssize_t at24_regmap_read(struct at24_data* mmc_mailbox,
                                char* buf,
                                unsigned int offset,
                                size_t count)
{
    unsigned long timeout, read_time;
    struct i2c_client* client;
    struct regmap* regmap;
    int ret;

    regmap = mmc_mailbox->regmap;
    client = mmc_mailbox->client;

    count = at24_adjust_read_count(mmc_mailbox, offset, count);

    timeout = jiffies + msecs_to_jiffies(at24_write_timeout);
    do {
        /*
     * The timestamp shall be taken before the actual operation
     * to avoid a premature timeout in case of high CPU load.
     */
        read_time = jiffies;

        ret = regmap_bulk_read(regmap, offset, buf, count);
        dev_dbg(&client->dev, "read %zu@%d --> %d (%ld)\n", count, offset, ret, jiffies);
        if (!ret)
            return count;

        usleep_range(1000, 1500);
    } while (time_before(read_time, timeout));

    return -ETIMEDOUT;
}

/*
 * Note that if the hardware write-protect pin is pulled high, the whole
 * chip is normally write protected. But there are plenty of product
 * variants here, including OTP fuses and partial chip protect.
 *
 * We only use page mode writes; the alternative is sloooow. These routines
 * write at most one page.
 */

static size_t at24_adjust_write_count(struct at24_data* mmc_mailbox,
                                      unsigned int offset,
                                      size_t count)
{
    unsigned int next_page;

    /* write_max is at most a page */
    if (count > mmc_mailbox->write_max)
        count = mmc_mailbox->write_max;

    /* Never roll over backwards, to the start of this page */
    next_page = roundup(offset + 1, mmc_mailbox->page_size);
    if (offset + count > next_page)
        count = next_page - offset;

    return count;
}

static ssize_t at24_regmap_write(struct at24_data* mmc_mailbox,
                                 const char* buf,
                                 unsigned int offset,
                                 size_t count)
{
    unsigned long timeout, write_time;
    struct i2c_client* client;
    struct regmap* regmap;
    int ret;

    regmap = mmc_mailbox->regmap;
    client = mmc_mailbox->client;
    count = at24_adjust_write_count(mmc_mailbox, offset, count);
    timeout = jiffies + msecs_to_jiffies(at24_write_timeout);

    do {
        /*
     * The timestamp shall be taken before the actual operation
     * to avoid a premature timeout in case of high CPU load.
     */
        write_time = jiffies;

        ret = regmap_bulk_write(regmap, offset, buf, count);
        dev_dbg(&client->dev, "write %zu@%d --> %d (%ld)\n", count, offset, ret, jiffies);
        if (!ret)
            return count;

        usleep_range(1000, 1500);
    } while (time_before(write_time, timeout));

    return -ETIMEDOUT;
}

/* For read/write accesses longer than 1 byte, set the "page lock" flag
 * This flag prevents the MMC from swapping the page, protecting the critical section
 */

#define MB_LOCK_OFFS 2047
#define MB_LOCK_FLAG 0x01

static bool lock_if_multiple(struct at24_data* mmc_mailbox, size_t count)
{
    uint8_t tmp;

    if (count <= 1) {
        return false;
    }
    tmp = MB_LOCK_FLAG;
    at24_regmap_write(mmc_mailbox, &tmp, MB_LOCK_OFFS, sizeof(tmp));
    //    dev_info(&mmc_mailbox->client->dev, "locked\n");
    return true;
}

static void unlock_if_locked(struct at24_data* mmc_mailbox, bool locked)
{
    uint8_t tmp;

    if (!locked) {
        return;
    }
    tmp = 0;
    at24_regmap_write(mmc_mailbox, &tmp, MB_LOCK_OFFS, sizeof(tmp));
    //    dev_info(&mmc_mailbox->client->dev, "unlocked\n");
}

static int at24_read(void* priv, unsigned int off, void* val, size_t count)
{
    struct at24_data* mmc_mailbox;
    struct device* dev;
    char* buf = val;
    int ret;
    bool locked;

    mmc_mailbox = priv;
    dev = &mmc_mailbox->client->dev;

    if (unlikely(!count))
        return count;

    if (off + count > mmc_mailbox->byte_len)
        return -EINVAL;

    ret = pm_runtime_get_sync(dev);
    if (ret < 0) {
        pm_runtime_put_noidle(dev);
        return ret;
    }

    /*
   * Read data from chip, protecting against concurrent updates
   * from this host, but not from other I2C masters.
   */
    mutex_lock(&mmc_mailbox->lock);
    //    dev_info(dev, "read %lu bytes at %u\n", count, off);
    locked = lock_if_multiple(mmc_mailbox, count);

    while (count) {
        ret = at24_regmap_read(mmc_mailbox, buf, off, count);
        if (ret < 0) {
            mutex_unlock(&mmc_mailbox->lock);
            pm_runtime_put(dev);
            return ret;
        }
        buf += ret;
        off += ret;
        count -= ret;
    }

    unlock_if_locked(mmc_mailbox, locked);
    mutex_unlock(&mmc_mailbox->lock);

    pm_runtime_put(dev);

    return 0;
}

static int at24_write(void* priv, unsigned int off, void* val, size_t count)
{
    struct at24_data* mmc_mailbox;
    struct device* dev;
    char* buf = val;
    int ret;
    bool locked;

    mmc_mailbox = priv;
    dev = &mmc_mailbox->client->dev;

    if (unlikely(!count))
        return -EINVAL;

    if (off + count > mmc_mailbox->byte_len)
        return -EINVAL;

    ret = pm_runtime_get_sync(dev);
    if (ret < 0) {
        pm_runtime_put_noidle(dev);
        return ret;
    }

    /*
   * Write data to chip, protecting against concurrent updates
   * from this host, but not from other I2C masters.
   */
    mutex_lock(&mmc_mailbox->lock);
    //    dev_info(dev, "write %lu bytes at %u\n", count, off);
    locked = lock_if_multiple(mmc_mailbox, count);

    while (count) {
        ret = at24_regmap_write(mmc_mailbox, buf, off, count);
        if (ret < 0) {
            mutex_unlock(&mmc_mailbox->lock);
            pm_runtime_put(dev);
            return ret;
        }
        buf += ret;
        off += ret;
        count -= ret;
    }

    unlock_if_locked(mmc_mailbox, locked);
    mutex_unlock(&mmc_mailbox->lock);

    pm_runtime_put(dev);

    return 0;
}

static struct at24_data* mmc_mb_pwroff_inst = NULL;

static void mmc_mailbox_do_poweroff(void)
{
#define MB_FPGA_STATUS_OFFS 2046
#define MB_FPGA_STATUS_SHDN_FINISHED BIT(2)

    uint8_t stat = MB_FPGA_STATUS_SHDN_FINISHED;

    if (!mmc_mb_pwroff_inst) {
        dev_err(&mmc_mb_pwroff_inst->client->dev, "no mailbox instance available\n");
        return;
    }

    dev_info(&mmc_mb_pwroff_inst->client->dev, "Sending SHDN_FINISHED to MMC\n");
    //    at24_write(mmc_mb_pwroff_inst, MB_FPGA_STATUS_OFFS, &stat, sizeof(stat));
    regmap_bulk_write(mmc_mb_pwroff_inst->regmap, MB_FPGA_STATUS_OFFS, &stat, sizeof(stat));
    mdelay(1000);

    WARN_ON(1);
}

static const struct at24_chip_data* at24_get_chip_data(struct device* dev)
{
    struct device_node* of_node = dev->of_node;
    const struct at24_chip_data* cdata;
    const struct i2c_device_id* id;

    id = i2c_match_id(mmc_mailbox_ids, to_i2c_client(dev));

    /*
   * The I2C core allows OF nodes compatibles to match against the
   * I2C device ID table as a fallback, so check not only if an OF
   * node is present but also if it matches an OF device ID entry.
   */
    if (of_node && of_match_device(mmc_mailbox_of_match, dev))
        cdata = of_device_get_match_data(dev);
    else if (id)
        cdata = (void*)id->driver_data;
    else
        cdata = NULL;

    if (!cdata)
        return ERR_PTR(-ENODEV);

    return cdata;
}

static int mmc_mailbox_probe(struct i2c_client* client)
{
    struct regmap_config regmap_config = {};
    struct nvmem_config nvmem_config = {};
    u32 byte_len, page_size;
    const struct at24_chip_data* cdata;
    struct device* dev = &client->dev;
    bool i2c_fn_i2c, i2c_fn_block;
    struct at24_data* mmc_mailbox;
    struct regmap* regmap;
    u8 test_byte;
    int err;

    i2c_fn_i2c = i2c_check_functionality(client->adapter, I2C_FUNC_I2C);
    i2c_fn_block = i2c_check_functionality(client->adapter, I2C_FUNC_SMBUS_WRITE_I2C_BLOCK);

    cdata = at24_get_chip_data(dev);
    if (IS_ERR(cdata))
        return PTR_ERR(cdata);

    err = device_property_read_u32(dev, "pagesize", &page_size);
    if (err)
        page_size = 16;

    err = device_property_read_u32(dev, "size", &byte_len);
    if (err)
        byte_len = cdata->byte_len;

    if (!i2c_fn_i2c && !i2c_fn_block)
        page_size = 1;

    if (!page_size) {
        dev_err(dev, "page_size must not be 0!\n");
        return -EINVAL;
    }

    if (!is_power_of_2(page_size))
        dev_warn(dev, "page_size looks suspicious (no power of 2)!\n");

    regmap_config.val_bits = 8;
    regmap_config.reg_bits = 16;
    regmap_config.disable_locking = true;

    regmap = devm_regmap_init_i2c(client, &regmap_config);
    if (IS_ERR(regmap))
        return PTR_ERR(regmap);

    mmc_mailbox = devm_kzalloc(dev, sizeof(mmc_mailbox), GFP_KERNEL);
    if (!mmc_mailbox)
        return -ENOMEM;

    mutex_init(&mmc_mailbox->lock);
    mmc_mailbox->byte_len = byte_len;
    mmc_mailbox->page_size = page_size;
    mmc_mailbox->client = client;
    mmc_mailbox->regmap = regmap;

    mmc_mailbox->write_max = min_t(unsigned int, page_size, mmc_mailbox_io_limit);
    if (!i2c_fn_i2c && mmc_mailbox->write_max > I2C_SMBUS_BLOCK_MAX)
        mmc_mailbox->write_max = I2C_SMBUS_BLOCK_MAX;

    nvmem_config.name = dev_name(dev);
    nvmem_config.dev = dev;
    nvmem_config.read_only = false;
    nvmem_config.root_only = false;
    nvmem_config.owner = THIS_MODULE;
    nvmem_config.compat = true;
    nvmem_config.base_dev = dev;
    nvmem_config.reg_read = at24_read;
    nvmem_config.reg_write = at24_write;
    nvmem_config.priv = mmc_mailbox;
    nvmem_config.stride = 1;
    nvmem_config.word_size = 1;
    nvmem_config.size = byte_len;

    mmc_mailbox->nvmem = devm_nvmem_register(dev, &nvmem_config);
    if (IS_ERR(mmc_mailbox->nvmem))
        return PTR_ERR(mmc_mailbox->nvmem);

    i2c_set_clientdata(client, mmc_mailbox);

    /* enable runtime pm */
    pm_runtime_set_active(dev);
    pm_runtime_enable(dev);

    /*
   * Perform a one-byte test read to verify that the
   * chip is functional.
   */
    err = at24_read(mmc_mailbox, 0, &test_byte, 1);
    pm_runtime_idle(dev);
    if (err) {
        pm_runtime_disable(dev);
        return -ENODEV;
    }

    dev_info(dev,
             "%u byte %s EEPROM, %u bytes/write\n",
             byte_len,
             client->name,
             mmc_mailbox->write_max);

    /* If a pm_power_off function has already been added, leave it alone */
    if (pm_power_off != NULL) {
        dev_err(dev, "pm_power_off function already registered\n");
        return 0;
    }
    mmc_mb_pwroff_inst = mmc_mailbox;
    pm_power_off = &mmc_mailbox_do_poweroff;

    return 0;
}

static int mmc_mailbox_remove(struct i2c_client* client)
{
    pm_runtime_disable(&client->dev);
    pm_runtime_set_suspended(&client->dev);

    if (pm_power_off == &mmc_mailbox_do_poweroff) {
        pm_power_off = NULL;
    }

    return 0;
}

static struct i2c_driver mmc_mailbox_driver = {
    .driver =
        {
            .name = "mmc_mailbox",
            .of_match_table = mmc_mailbox_of_match,
        },
    .probe_new = mmc_mailbox_probe,
    .remove = mmc_mailbox_remove,
    .id_table = mmc_mailbox_ids,
};

static int __init mmc_mailbox_init(void)
{
    if (!mmc_mailbox_io_limit) {
        pr_err("mmc_mailbox: mmc_mailbox_io_limit must not be 0!\n");
        return -EINVAL;
    }

    mmc_mailbox_io_limit = rounddown_pow_of_two(mmc_mailbox_io_limit);
    return i2c_add_driver(&mmc_mailbox_driver);
}
module_init(mmc_mailbox_init);

static void __exit mmc_mailbox_exit(void)
{
    i2c_del_driver(&mmc_mailbox_driver);
}
module_exit(mmc_mailbox_exit);

MODULE_DESCRIPTION("Driver for DMMC-STAMP I2C Mailbox");
MODULE_AUTHOR("Patrick Huesmann");
MODULE_LICENSE("GPL");
