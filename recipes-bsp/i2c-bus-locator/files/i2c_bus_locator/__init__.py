#! /usr/bin/env python3

"""
Copyright (c) 2021 Deutsches Elektronen-Synchrotron DESY

Bus numbers in Linux are sometimes shuffled around. For example, when an I2C
device is added to the Programmable Logic (PL) and the device tree, it will
"push" all other devices up by with their bus numbers.

This means that in such an dynamic environment, relaying on I2C bus numbers
is not good enough.

This script provides a similar feature than manually looking ath the output
of `i2cdetect -l`. For example, if we know that out our board the device
is attached to the first I2C adapter on PS (provided by Cadence), we know
that we should use bus number 2:

```
# i2cdetect -l
i2c-3	i2c       	Cadence I2C at ff030000         	I2C adapter
i2c-4	i2c       	ZynqMP DP AUX                   	I2C adapter
i2c-2	i2c       	Cadence I2C at ff020000         	I2C adapter
i2c-0	i2c       	xiic-i2c                        	I2C adapter
```

"""

import os
import struct
from typing import List, Set, Dict, Tuple, Optional


def i2c_bus_locator(
    compat: str = None, addr: int = None, verbose: bool = False
) -> List[int]:
    """Get all I2C buses which match the specified criteria.

    If all criteria are None, return all buses (which have at least an
    entry in the device tree).
    """

    SYSFS_DIR = "/sys/class/i2c-adapter"

    ret_list = []

    adpts = os.listdir(SYSFS_DIR)

    for adpt in adpts:
        # get compatible string
        adpt_comp_file = os.path.join(SYSFS_DIR, adpt, "of_node/compatible")
        try:
            adpt_compat = open(adpt_comp_file, "r").read()
            if verbose:
                print("i2c_bus_locator: compat = {}".format(adpt_compat))
        except FileNotFoundError:
            if verbose:
                print("i2c_bus_locator: could not open 'compatible' for %s" % adpt)
            continue

        # get address
        adpt_addr_file = os.path.join(SYSFS_DIR, adpt, "of_node/reg")
        try:
            adpt_reg = open(adpt_addr_file, "rb").read()
            p_len = struct.calcsize("P")
            adpt_addr_bytes = adpt_reg[0:p_len]
            # Device Tree is always big-endian
            fmt = ">Q" if p_len == 8 else ">L"
            adpt_addr = struct.unpack(fmt, adpt_addr_bytes)[0]
            if verbose:
                print("i2c_bus_locator: addr = 0x{:x}".format(adpt_addr))

        except FileNotFoundError:
            if verbose:
                print("i2c_bus_locator: could not open 'reg' for %s" % adpt)
            continue

        # determine if this is what we are looking for
        comp_ok = compat is None or adpt_compat.find(compat) == 0
        addr_ok = addr is None or adpt_addr == addr
        if comp_ok and addr_ok:
            adpt_bus_nr = adpt.split("-")[1]
            ret_list.append(int(adpt_bus_nr))

    return ret_list
