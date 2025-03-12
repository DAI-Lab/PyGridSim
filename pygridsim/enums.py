from enum import Enum
import pygridsim.defaults as defaults

# todo: update to have a name so that users can query from name
class SourceType(Enum):
    TURBINE = defaults.TURBINE_BASE_KV
    SOLAR_PANEL = defaults.SOLAR_PANEL_BASE_KV

class LineType(Enum):
    LV_LINE = defaults.LV_LINE_LENGTH
    MV_LINE = defaults.MV_LINE_LENGTH
    HV_LINE = defaults.HV_LINE_LENGTH

class LoadType(Enum):
    HOUSE = {"kV": defaults.HOUSE_KV, "kW": defaults.HOUSE_KW, "kvar": defaults.HOUSE_KVAR}
    COMMERCIAL = {"kV": defaults.COMMERCIAL_KV, "kW": defaults.COMMERCIAL_KW, "kvar": defaults.COMMERCIAL_KVAR}
    INDUSTRIAL = {"kV": defaults.INDUSTRIAL_KV, "kW": defaults.INDUSTRIAL_KW, "kvar": defaults.INDUSTRIAL_KVAR}

class GeneratorType(Enum):
    SMALL = {"kV": defaults.SMALL_GEN_KV, "kW": defaults.SMALL_GEN_KW}
    LARGE = {"kV": defaults.LARGE_GEN_KV, "kW": defaults.LARGE_GEN_KW}
    INDUSTRIAL = {"kV": defaults.INDUSTRIAL_GEN_KV, "kW": defaults.INDUSTRIAL_GEN_KW}