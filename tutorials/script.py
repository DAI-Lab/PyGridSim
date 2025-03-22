#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygridsim.core import PyGridSim

circuit = PyGridSim()
circuit.update_source(source_type="turbine")
circuit.add_load_nodes(load_type="house", num=10)
circuit.add_PVSystem(load_nodes=["load0", "load1", "load2"], num_panels=10) # 10 solar panels to first three houses
circuit.add_generator(num=2, gen_type="small")
circuit.add_lines([("source", "load0"), ("generator0", "load0"), ("generator5", "source")])
circuit.solve()
print(circuit.results())