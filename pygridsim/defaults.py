"""
Set any defaults (i.e. default source voltage, default node load etc.)
"""
from altdss import Connection

"""
Overall Defaults, used for load, sources, lines, etc.
https://www.anker.com/blogs/home-power-backup/electricity-usage-how-much-energy-does-an-average-house-use
"""
PHASES = 1
FREQUENCY = 60

"""
Load Nodes
kW: around 30 kWH a day, divide by 24 hours
kVar is like around 0.2 or 0.1 of what kVar is
"""
HOUSE_KV = [.12, .24]
HOUSE_KW = [1, 1.5]
HOUSE_KVAR = [0.5, 1]

COMMERCIAL_KV = [.24, .48]
COMMERCIAL_KW = [10, 50]
COMMERCIAL_KVAR = [5, 10]

INDUSTRIAL_KV = [4.16, 34.5]
INDUSTRIAL_KW = [200, 10000]
INDUSTRIAL_KVAR = [150, 480]

"""
Source Nodes (including other form of sources, like PVSystem)
"""
IMPEDANCE = 0.0001
TURBINE_BASE_KV = [1, 3]
POWER_PLANT_KV = [10, 20]
LV_SUBSTATION_BASE_KV = [0.2, 0.4]
MV_SUBSTATION_BASE_KV = [6, 35]
HV_SUBSTATION_BASE_KV = [66, 500]
SHV_SUBSTATION_BASE_KV = [500, 1000]

SOLAR_PANEL_BASE_KV = [0.2, 0.4]  # per solar panel
"""
Generator default values (small, large, industrial)
"""
SMALL_GEN_KV = [0.2, 0.6]
LARGE_GEN_KV = [1, 35]
INDUSTRIAL_GEN_KV = [35, 100]
SMALL_GEN_KW = [2, 5]
LARGE_GEN_KW = [5, 10]
INDUSTRIAL_GEN_KW = [10, 20]

"""
Units: KM
LV = Low Voltage, MV = Medium Voltage
"""
LV_LINE_LENGTH = [30, 60]
MV_LINE_LENGTH = [60, 160]
HV_LINE_LENGTH = [160, 300]

"""
Transformers
"""
NUM_WINDINGS = 2
XHL = 2
PRIMARY_CONN = Connection.delta
SECONDARY_CONN = Connection.wye

"""
Valid parameter lists
"""
IMPEDANCE_PARAMS = ["R0", "R1", "X0", "X1"]

VALID_LOAD_PARAMS = ["kV", "kW", "kvar", "phases"]
VALID_SOURCE_PARAMS = ["kV", "phases", "frequency"] + IMPEDANCE_PARAMS
VALID_LINE_TRANSFORMER_PARAMS = ["length", "XHL", "Conns"]
VALID_PV_PARAMS = ["kV", "phases"]
VALID_GENERATOR_PARAMS = ["kV", "kW", "phases"]
