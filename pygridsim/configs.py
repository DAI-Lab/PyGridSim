from pygridsim.enums import *
from pygridsim.defaults import *

LOAD_CONFIGURATIONS = {
    LoadType.HOUSE: {
        "kV": HOUSE_KV, 
        "kW": HOUSE_KW, 
        "kvar": HOUSE_KVAR
    },
    LoadType.COMMERCIAL: {
        "kV": COMMERCIAL_KV,
        "kW": COMMERCIAL_KW, 
        "kvar": COMMERCIAL_KVAR
    },
    LoadType.INDUSTRIAL: {
        "kV": INDUSTRIAL_KV, 
        "kW": INDUSTRIAL_KW, 
        "kvar": INDUSTRIAL_KVAR
    }
}

SOURCE_CONFIGURATIONS = {
    SourceType.TURBINE: {
        "kV": TURBINE_BASE_KV
    },
    SourceType.POWER_PLANT: {
        "kV": POWER_PLANT_KV
    },
    SourceType.LV_SUBSTATION: {
        "kV": LV_SUBSTATION_BASE_KV
    },
    SourceType.MV_SUBSTATION: {
        "kV": MV_SUBSTATION_BASE_KV
    },
    SourceType.HV_SUBSTATION: {
        "kV": HV_SUBSTATION_BASE_KV
    },
    SourceType.SHV_SUBSTATION: {
        "kV": SHV_SUBSTATION_BASE_KV
    },
}

LINE_CONFIGURATIONS = {
    LineType.LV_LINE: {
        "length": LV_LINE_LENGTH
    },
    LineType.MV_LINE: {
        "length": MV_LINE_LENGTH
    },
    LineType.HV_LINE: {
        "length": HV_LINE_LENGTH
    }
}

GENERATOR_CONFIGURATIONS = {
    GeneratorType.SMALL: {
        "kV": SMALL_GEN_KV, 
        "kW": SMALL_GEN_KW, 
    },
    GeneratorType.LARGE: {
        "kV": LARGE_GEN_KV, 
        "kW": LARGE_GEN_KW, 
    },
    GeneratorType.INDUSTRIAL: {
        "kV": INDUSTRIAL_GEN_KV, 
        "kW": INDUSTRIAL_GEN_KW, 
    }
}