from enum import Enum
import pygridsim.defaults as defaults

class SourceType(Enum):
    TURBINE = defaults.TURBINE_BASE_KV
    SOLAR_PANEL = defaults.SOLAR_PANEL_BASE_KV

class LineType(Enum):
    LV_LINE = defaults.LV_LINE_LENGTH
    MV_LINE = defaults.MV_LINE_LENGTH
    HV_LINE = defaults.HV_LINE_LENGTH

class LoadType(Enum):
    HOUSE = {"kV": defaults.HOUSE_KV, "kW": defaults.HOUSE_KW, "kVar": defaults.HOUSE_KVAR}
    COMMERCIAL = {"kV": defaults.COMMERCIAL_KV, "kW": defaults.COMMERCIAL_KW, "kVar": defaults.COMMERCIAL_KVAR}
    INDUSTRIAL = {"kV": defaults.INDUSTRIAL_KV, "kW": defaults.INDUSTRIAL_KW, "kVar": defaults.INDUSTRIAL_KVAR}