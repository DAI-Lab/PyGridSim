from enum import Enum


class SourceType(Enum):
    TURBINE = "turbine"
    POWER_PLANT = "powerplant"
    LV_SUBSTATION = "lvsub"
    MV_SUBSTATION = "mvsub"
    HV_SUBSTATION = "hvsub"
    SHV_SUBSTATION = "shvsub"


class LineType(Enum):
    LV_LINE = "lv"
    MV_LINE = "mv"
    HV_LINE = "hv"


class LoadType(Enum):
    HOUSE = "house"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"


class GeneratorType(Enum):
    SMALL = "small"
    LARGE = "large"
    INDUSTRIAL = "industrial"
