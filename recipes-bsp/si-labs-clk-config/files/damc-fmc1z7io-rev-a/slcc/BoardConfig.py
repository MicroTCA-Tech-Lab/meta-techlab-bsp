# Board Config for DAMC-FMC1Z7IO

from i2c_bus_locator import i2c_bus_locator

CLK_BUS = i2c_bus_locator(compat="cdns", addr=0xe0004000)[0]
