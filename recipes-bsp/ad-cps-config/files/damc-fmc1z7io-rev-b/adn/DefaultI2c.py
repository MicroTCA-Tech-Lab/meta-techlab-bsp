from i2c_bus_locator import i2c_bus_locator

DEFAULT_I2C_BUS = i2c_bus_locator(compat="cdns", addr=0xe0004000)[0]
