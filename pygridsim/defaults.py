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

"""
Overall Defaults, used for load, sources, lines, etc.
https://www.anker.com/blogs/home-power-backup/electricity-usage-how-much-energy-does-an-average-house-use
"""
PHASES = 1
FREQUENCY = 60

"""
Load Nodes
"""
HOUSE_KV = [120, 240]
HOUSE_KW = [1, 1.4]
HOUSE_KVAR = 0.6 # unclear

"""
Source Nodes
TODO also fuel cells, other less common forms of energy later
"""

TURBINE_BASE_KV = [0.55,0.7]
SOLAR_PANEL_BASE_KV = [0.0005, 0.0006] # per solar panel

"""
Units: KM
LV = Low Voltage, MV = Medium Voltage
Based on IEEE standards
"""
RESIDENTIAL_LV_LINE_LENGTH = [0.05, 0.3]
RESIDENTIAL_MV_LINE_LENGTH = [1, 10]
RURAL_LV_LINE_LENGTH = [0.1 ,0.5]
RURAL_MV_LINE_LENGTH = [10, 50]
INDUSTRIAL_LV_LINE_LENGTH = [0.01, 0.2]
INDUSTRIAL_MV_LINE_LENGTH = [1,5]
URBAN_LV_LINE_LENGTH = [0.02, 0.2]
URBAN_MV_LINE_LENGTH = [1,10]