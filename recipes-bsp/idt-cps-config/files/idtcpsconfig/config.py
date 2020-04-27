#! /usr/bin/env python3

from idtcpsconfig.PortConfig import PortConfig
from idtcpsconfig.ZupPortName import ZupPortName

configs = [PortConfig(0, 0, 0, 0) for _ in range(16)]

configs[ZupPortName.CPS_GC1] = configs[ZupPortName.CPS_GC1]._replace(source=ZupPortName.TCLKA)._replace(output=1)
configs[ZupPortName.CPS_GC2] = configs[ZupPortName.CPS_GC2]._replace(source=ZupPortName.MPLL2CPS)._replace(output=1)
configs[ZupPortName.MPLL2CPS] = configs[ZupPortName.MPLL2CPS]._replace(term=1)

config_bytes = b"".join([ci.to_byte() for ci in configs])

