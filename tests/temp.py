# -*- coding: utf-8 -*-
from altdss import altdss
from altdss import AltDSS, Transformer, Vsource, Load, LoadModel, LoadShape
from dss.enums import LineUnits, SolveModes
"""
this is from colab stuff, delete later
"""

altdss('new circuit.IEEE13Nodeckt')

# create voltage source
source1 = altdss.Vsource[0]
source1.Bus1 = 'SourceBus'
source1.BasekV = 0.6
source1.Phases = 3
source1.Frequency = 60

# create load
load1 : Load = altdss.Load.new('load1')
load1.Bus1 = 'LoadBus'
load1.Phases = 3
load1.kV = 200
load1.kW = 1.2
load1.kvar = 0.6

# line between voltage source and load
line1 = altdss.Line.new('line1')
line1.Phases = 3
line1.Bus1 = 'SourceBus'
line1.Bus2 = 'LoadBus'
line1.Length = 0.1
line1.Units = LineUnits.km

# "solve" the circuit
altdss.Solution.Solve()
print(altdss.BusVMag())