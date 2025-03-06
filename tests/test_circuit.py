#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygridsim.core import PyGridSim
from pygridsim.enums import LineType, SourceType, LoadType
from altdss import altdss
from altdss import Connection


"""Tests for `pygridsim` package."""

import unittest

# from pygridsim import pygridsim


class TestDefaultRangeCircuit(unittest.TestCase):
    """
    All of these tests work with default range circuits (i.e. enum inputs)
    can't verify exact value, but still should check in range
    """
    circuit = PyGridSim()

    def setUp(self):
        """Set up test fixtures, if any."""
        print("\nTest", self._testMethodName)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        #altdss.ClearAll()

    def test_000_basic(self):
        circuit = PyGridSim()
        circuit.add_source_nodes()
        circuit.add_load_nodes()
        circuit.add_lines([("source", "load0")])
        circuit.solve()
        print(circuit.results(["Voltages"]))
        circuit.clear()

    def test_001_one_source_one_load(self):
        circuit = PyGridSim()
        circuit.add_source_nodes(source_type=SourceType.TURBINE)
        circuit.add_load_nodes(num=1, load_type=LoadType.HOUSE)
        circuit.add_lines([("source", "load0")], LineType.MV_LINE)
        #circuit.add_transformers([("source", "load0")], params={"Conns": [Connection.wye, Connection.delta]})
        print("Load Nodes:", circuit.view_load_nodes())
        print("Source Nodes:", circuit.view_source_node())
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()
    
    def test_002_one_source_one_load_no_transformer(self):
        # doesn't throw error, but should have stranger output VMag
        circuit = PyGridSim()
        circuit.add_source_nodes(source_type=SourceType.TURBINE)
        circuit.add_load_nodes(num=1, load_type=LoadType.HOUSE)
        circuit.add_lines([("source", "load0")], LineType.MV_LINE, transformer=False)
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()

    def test_003_one_source_one_load_exhaustive(self):
        for line_type in LineType:
            for source_type in SourceType:
                for load_type in LoadType:
                    circuit = PyGridSim()
                    circuit.add_source_nodes(source_type=source_type)
                    circuit.add_load_nodes(num=1, load_type=load_type)
                    circuit.add_lines([("source", "load0")], line_type)
                    circuit.solve()
                    print("LineType:", line_type, "SourceType", source_type, "LoadType", load_type)
                    print(circuit.results(["Voltages", "Losses"]))
                    circuit.clear()


    def test_004_one_source_multi_load(self):
        circuit = PyGridSim()
        circuit.add_source_nodes(num_in_batch=10, source_type=SourceType.SOLAR_PANEL)
        circuit.add_load_nodes(num=4, load_type=LoadType.HOUSE)
        circuit.add_lines([("source", "load0"), ("source", "load3")], LineType.HV_LINE)
        circuit.solve()
        print(circuit.results(["Voltages"]))
        circuit.clear()
    
    def test_005_bad_query(self):
        circuit = PyGridSim()
        circuit.add_source_nodes()
        circuit.add_load_nodes()
        circuit.add_lines([("source", "load0")])
        circuit.solve()
        print(circuit.results(["BadQuery"]))

    def test_006_multi_source_bad(self):
        circuit = PyGridSim()
        #circuit.add_source_nodes(num_in_batch=10, num=2, source_type=SourceType.SOLAR_PANEL)
        #circuit.add_load_nodes(num=1, load_type=LoadType.HOUSE)
        #circuit.add_lines([("source", "load0")], LineType.HV_LINE)
        #circuit.solve()
        # TODO: can add assert to make sure it's in reasonable range?
    
    def test_007_export(self):
        circuit = PyGridSim()
        circuit.add_source_nodes()
        circuit.add_load_nodes()
        circuit.add_lines([("source", "load0")])
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"], export_path="sim.json"))


class TestCustomizedCircuit(unittest.TestCase):
    """
    Test with exact parameters entered. won't be the typical client use case, but should check that these matche exact values
    """

    def setUp(self):
        """Set up test fixtures, if any."""
        print("\nTest", self._testMethodName)


    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_100_one_source_one_load(self):
        circuit = PyGridSim()
        circuit.add_source_nodes(params={"kV": 100})
        circuit.add_load_nodes(num=1, params={"kV": 10, "kW": 20, "kVar":1})
        circuit.add_lines([("source", "load0")], params={"length": 20})
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()

    def test_100_one_source_multi_load(self):
        """
        Creates 10 loads, some of which are connected to source. all loads and lines here have the same params
        """
        circuit = PyGridSim()
        circuit.add_source_nodes(params={"kV": 100})
        circuit.add_load_nodes(num=10, params={"kV": 10, "kW": 20, "kVar":1})
        circuit.add_lines([("source", "load0"), ("source", "load4"), ("source", "load6")], params={"length": 20})
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()
    
    def test_101_bad_parameter(self):
        """
        Should error with a bad parameter and tell the user which parameter is bad
        """
        circuit = PyGridSim()
        with self.assertRaises(KeyError):
            circuit.add_source_nodes(params={"kV": 50, "badParam": 100})

    def test_102_negative_inputs(self):
        """
        Should error with negative kv or negative length
        """
        circuit = PyGridSim()
        
        with self.assertRaises(Exception):
            # openDSS has its own exception for this case
            circuit.add_load_nodes(params={"kV": -1})
        
        with self.assertRaises(ValueError):
            circuit.add_source_nodes(params={"kV": -1})
        
        # properly add load and source, then create invalid line
        with self.assertRaises(ValueError):
            circuit.add_lines([("source", "load0")], params={"length": -100})

    def test_103_invalid_nodes_in_line(self):
        circuit = PyGridSim()
        circuit.add_load_nodes()
        circuit.add_source_nodes()
        with self.assertRaises(ValueError):
            # only has source, load0 for now but tries to add another one
            circuit.add_lines([("source", "load5")])


class TestLargeCircuit(unittest.TestCase):
    """
    Test very large circuit (i.e. to the size of a neighborhood)
    """
    def setUp(self):
        """Set up test fixtures, if any."""
        print("\nTest", self._testMethodName)


    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass
