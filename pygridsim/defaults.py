"""
Set any defaults (i.e. default source voltage, default node load etc.)
Will start with things like HOUSE_KV to define typical load of a house (perhaps with some variance)

Source:
Define default values for a few types of objects.
In a neighborhood the main ones are
solar panels, wind turbines

Load:
Define for a typical house, using statistics
https://forum.allaboutcircuits.com/threads/what-is-the-actual-household-voltage-110-115-120-220-240.3320/
https://www.eia.gov/energyexplained/use-of-energy/electricity-use-in-homes.php?utm_source=chatgpt.com

In the second iteration
- implement the typical LoadShape in the house
- some randomness to cover the standard distribution of houses, not all the averages

For now, many of them are listed as tuples - lower end, higher end.
TODO: make generate function that does Math.rand for in the range (later: improve distribution to be non-uniform)
"""
from altdss import altdss
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
HOUSE_KVAR = [0.5, 1] # unclear

COMMERCIAL_KV = [.24, .48]
COMMERCIAL_KW = [10, 50]
COMMERCIAL_KVAR = [5, 10]

INDUSTRIAL_KV = [.24, .48]
INDUSTRIAL_KW = [30, 100]
INDUSTRIAL_KVAR = [20, 25]

"""
Source Nodes
TODO also fuel cells, other less common forms of energy later
"""

TURBINE_BASE_KV = [3000,4000]
SOLAR_PANEL_BASE_KV = [0.2, 0.4] # per solar panel

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