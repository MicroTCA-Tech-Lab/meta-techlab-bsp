# Board Config for DAMC-MOTCTRL

from i2c_bus_locator import i2c_bus_locator

CLK_BUS = i2c_bus_locator(compat="cdns", addr=0xff020000)[0]
