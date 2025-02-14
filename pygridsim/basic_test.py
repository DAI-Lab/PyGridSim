from core import PyGridSim
from enums import LineType, SourceType, LoadType
from altdss import altdss

"""
Goal: to be able to very easily make a scalable circuit that represents a residential district
"""

circuit = PyGridSim()
circuit.add_source_nodes(num_in_batch=10, source_type=SourceType.SOLAR_PANEL)
circuit.add_load_nodes(num=4, load_type=LoadType.HOUSE)
circuit.add_lines([("source", "load0"), ("source", "load3")], LineType.MV_LINE)
circuit.add_transformers([("source", "load0")])
circuit.solve()
print(circuit.results(["BusVMag"]))

"""
print(circuit.view_load_nodes())
print(circuit.view_source_node())
"""