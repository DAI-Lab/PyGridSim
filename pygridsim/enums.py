from enum import Enum
import defaults

class SourceType(Enum):
    TURBINE = defaults.TURBINE_BASE_KV
    SOLAR_PANEL = defaults.SOLAR_PANEL_BASE_KV

class LineType(Enum):
    RESIDENTIAL_LV_LINE = defaults.RESIDENTIAL_LV_LINE_LENGTH
    RESIDENTIAL_MV_LINE = defaults.RESIDENTIAL_MV_LINE_LENGTH
    RURAL_LV_LINE = defaults.RURAL_LV_LINE_LENGTH
    RURAL_MV_LINE = defaults.RURAL_MV_LINE_LENGTH
    INDUSTRIAL_LV_LINE = defaults.INDUSTRIAL_LV_LINE_LENGTH
    INDUSTRIAL_MV_LINE = defaults.INDUSTRIAL_MV_LINE_LENGTH
    URBAN_LV_LINE = defaults.URBAN_LV_LINE_LENGTH
    URBAN_MV_LINE = defaults.INDUSTRIAL_MV_LINE_LENGTH