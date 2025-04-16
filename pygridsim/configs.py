import pygridsim.defaults as defaults
from pygridsim.enums import GeneratorType, LineType, LoadType, SourceType

LOAD_CONFIGURATIONS = {
    LoadType.HOUSE: {
        "kV": defaults.HOUSE_KV,
        "kW": defaults.HOUSE_KW,
        "kvar": defaults.HOUSE_KVAR
    },
    LoadType.COMMERCIAL: {
        "kV": defaults.COMMERCIAL_KV,
        "kW": defaults.COMMERCIAL_KW,
        "kvar": defaults.COMMERCIAL_KVAR
    },
    LoadType.INDUSTRIAL: {
        "kV": defaults.INDUSTRIAL_KV,
        "kW": defaults.INDUSTRIAL_KW,
        "kvar": defaults.INDUSTRIAL_KVAR
    }
}

SOURCE_CONFIGURATIONS = {
    SourceType.TURBINE: {
        "kV": defaults.TURBINE_BASE_KV
    },
    SourceType.POWER_PLANT: {
        "kV": defaults.POWER_PLANT_KV
    },
    SourceType.LV_SUBSTATION: {
        "kV": defaults.LV_SUBSTATION_BASE_KV
    },
    SourceType.MV_SUBSTATION: {
        "kV": defaults.MV_SUBSTATION_BASE_KV
    },
    SourceType.HV_SUBSTATION: {
        "kV": defaults.HV_SUBSTATION_BASE_KV
    },
    SourceType.SHV_SUBSTATION: {
        "kV": defaults.SHV_SUBSTATION_BASE_KV
    },
}

LINE_CONFIGURATIONS = {
    LineType.LV_LINE: {
        "length": defaults.LV_LINE_LENGTH
    },
    LineType.MV_LINE: {
        "length": defaults.MV_LINE_LENGTH
    },
    LineType.HV_LINE: {
        "length": defaults.HV_LINE_LENGTH
    }
}

GENERATOR_CONFIGURATIONS = {
    GeneratorType.SMALL: {
        "kV": defaults.SMALL_GEN_KV,
        "kW": defaults.SMALL_GEN_KW,
    },
    GeneratorType.LARGE: {
        "kV": defaults.LARGE_GEN_KV,
        "kW": defaults.LARGE_GEN_KW,
    },
    GeneratorType.INDUSTRIAL: {
        "kV": defaults.INDUSTRIAL_GEN_KV,
        "kW": defaults.INDUSTRIAL_GEN_KW,
    }
}

NAME_TO_CONFIG = {
    "load": LOAD_CONFIGURATIONS,
    "source": SOURCE_CONFIGURATIONS,
    "generator": GENERATOR_CONFIGURATIONS,
    "line": LINE_CONFIGURATIONS
}
