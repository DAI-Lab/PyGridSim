from core import PyGridSim
from enums import LineType, SourceType

"""
Goal: to be able to very easily make a scalable circuit that represents a residential district
"""

circuit = PyGridSim()
circuit.add_source_nodes(num=1)
circuit.add_load_nodes(num=4)
circuit.add_lines([("source0", "load0"), ("source0", "load2")], LineType.INDUSTRIAL_LV_LINE)
circuit.solve()
print(circuit.results(["BusVMag"]))

# using solar panel leads to a lot lower kv obviously