#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from pygridsim.core import PyGridSim
from pygridsim.enums import GeneratorType, LineType, LoadType, SourceType

"""Tests for `pygridsim` package."""


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

    def test_000_basic(self):
        circuit = PyGridSim()
        circuit.update_source()
        circuit.add_load_nodes()
        circuit.add_lines([("source", "load0")])
        circuit.solve()
        print(circuit.results(["Voltages"]))
        circuit.clear()

    def test_001_one_source_one_load(self):
        circuit = PyGridSim()
        circuit.update_source(source_type="turbine")
        circuit.add_load_nodes(num=1, load_type="house")
        circuit.add_lines([("source", "load0")], "MV")
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()

    def test_002_one_source_one_load_no_transformer(self):
        # doesn't throw error, but should have stranger output VMag
        circuit = PyGridSim()
        circuit.update_source(source_type="turbine")
        circuit.add_load_nodes(num=1, load_type="house")
        circuit.add_lines([("source", "load0")], "MV", transformer=False)
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()

    def test_003_one_source_one_load_exhaustive(self):
        for line_type in LineType:
            for source_type in SourceType:
                for load_type in LoadType:
                    circuit = PyGridSim()
                    circuit.update_source(source_type=source_type.value)
                    circuit.add_load_nodes(num=1, load_type=load_type.value)
                    circuit.add_lines([("source", "load0")], line_type.value)
                    circuit.solve()
                    circuit.clear()

    def test_004_one_source_multi_load(self):
        circuit = PyGridSim()
        circuit.update_source(source_type="turbine")
        circuit.add_load_nodes(num=4, load_type="house")
        circuit.add_lines([("source", "load0"), ("source", "load3")], "HV")
        circuit.solve()
        print(circuit.results(["Voltages"]))
        circuit.clear()

    def test_005_bad_query(self):
        circuit = PyGridSim()
        circuit.update_source()
        circuit.add_load_nodes()
        circuit.add_lines([("source", "load0")])
        circuit.solve()
        print(circuit.results(["BadQuery"]))

    def test_006_update_multiple_source(self):
        circuit = PyGridSim()
        circuit.update_source(source_type="turbine")
        circuit.add_load_nodes(num=1, load_type="house")
        circuit.update_source(source_type="turbine")
        circuit.add_lines([("source", "load0")], "HV")
        circuit.solve()
        print(circuit.results(["Voltages"]))

    def test_007_export(self):
        circuit = PyGridSim()
        circuit.update_source(params={"kV": 10})
        circuit.add_load_nodes(params={"kV": 5, "kW": 10, "kvar": 2})
        circuit.add_lines([("source", "load0")], params={"length": 2})
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"], export_path="sim.json"))

    def test_008_PVsystem(self):
        circuit = PyGridSim()
        circuit.update_source()
        circuit.add_load_nodes(num=2)
        circuit.add_PVSystems(load_nodes=["load0", "load1"], num_panels=5)
        circuit.add_lines([("source", "load0")])
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))

    def test_009_generator(self):
        circuit = PyGridSim()
        circuit.update_source()
        circuit.add_load_nodes()
        circuit.add_generators(num=3, gen_type="small")
        circuit.add_lines([("source", "load0"), ("generator0", "load0")])
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))

    def test_010_many_sources(self):
        circuit = PyGridSim()
        circuit.update_source(source_type="powerplant")
        circuit.add_load_nodes(num=3)
        circuit.add_PVSystems(load_nodes=["load1", "load2"], num_panels=10)
        circuit.add_generators(num=3, gen_type="small")
        circuit.update_source(source_type="turbine")  # change to a turbine source midway
        circuit.add_generators(num=4, gen_type="large")
        circuit.add_lines([("source", "load0"), ("generator0", "load0"), ("generator5", "source")])
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))

    def test_011_configs(self):
        circuit = PyGridSim()

        # LOAD CONFIG
        # should work, because not case sensitive
        circuit.add_load_nodes(num=2, load_type="HOUSE")
        circuit.add_load_nodes(num=2, load_type="hoUSE")
        # should fail, invalid load_type value
        with self.assertRaises(KeyError):
            circuit.add_load_nodes(num=2, load_type="badloadtype")
        # don't want loadtype input, just string
        with self.assertRaises(Exception):
            circuit.add_load_nodes(num=2, load_type=LoadType.HOUSE)

        # LINE CONFIG
        # works, because not case sensitive
        circuit.add_lines([("source", "load0")], line_type="HV")
        # don't want linetype input, just string
        with self.assertRaises(Exception):
            circuit.add_lines([("source", "load0")], line_type=LineType.HV_LINE)

        # GENERATOR CONFIG
        # works, because not case sensitive
        circuit.add_generators(num=3, gen_type="SMALl")
        # don't want linetype input, just string
        with self.assertRaises(Exception):
            circuit.add_generators(num=3, gen_type=GeneratorType.SMALL)

        # SOURCE CONFIG
        # works, because not case sensitive
        circuit.update_source(source_type="turBINE")
        # source type as first param, ignores spaces, this should also work
        circuit.update_source("power plant")
        # don't want linetype input, just string
        with self.assertRaises(Exception):
            circuit.update_source(source_type=SourceType.TURBINE)

    def test_012_all_results(self):
        circuit = PyGridSim()
        circuit.update_source()
        circuit.add_load_nodes()
        circuit.add_generators(num=2, gen_type="small")
        circuit.add_lines([("source", "load0"), ("generator0", "load0")])
        circuit.solve()
        # Should be flexible with capitalization, spaces
        queries = ["Voltages", "losses", "Total Power"]
        # Add "partial" queries to just parts of losses/total power
        queries += ["realpowerloss", "reactive Loss", "Active Power", "reactivepower"]
        print(circuit.results(queries))


class TestCustomizedCircuit(unittest.TestCase):
    """
    Test with exact parameters entered.
    """

    def setUp(self):
        """Set up test fixtures, if any."""
        print("\nTest", self._testMethodName)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_100_one_source_one_load(self):
        circuit = PyGridSim()
        circuit.update_source(params={"kV": 100, "R0": 0.1, "R1": 0.2, "X0": 0.3, "X1": 0.4})
        circuit.add_load_nodes(num=1, params={"kV": 10, "kW": 20, "kvar": 1})
        circuit.add_lines([("source", "load0")], params={"length": 20})
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()

    def test_100_one_source_multi_load(self):
        """
        Creates 10 loads, some of which are connected to source.
        All loads and lines here have the same params.
        """
        circuit = PyGridSim()
        circuit.update_source(params={"kV": 100})
        circuit.add_load_nodes(num=10, params={"kV": 10, "kW": 20, "kvar": 1})
        circuit.add_lines([("source", "load0"), ("source", "load4"), ("source", "load6")],
                          params={"length": 20})
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()

    def test_101_bad_parameter(self):
        """
        Should error with a bad parameter and tell the user which parameter is bad
        """
        circuit = PyGridSim()
        with self.assertRaises(KeyError):
            circuit.update_source(params={"kV": 50, "badParam": 100})
        with self.assertRaises(KeyError):
            circuit.add_load_nodes(num=4, params={"badParam": 100})
        # add load nodes so we can test pv system erroring
        circuit.add_load_nodes(num=2, params={"kV": 10, "kW": 20, "kvar": 1})
        with self.assertRaises(KeyError):
            circuit.add_generators(num=4, params={"badParam": 100})
        with self.assertRaises(KeyError):
            circuit.add_PVSystems(load_nodes=["load0"], params={"badParam": 100}, num_panels=4)

    def test_102_negative_inputs(self):
        """
        Should error with negative kv or negative length
        """
        circuit = PyGridSim()

        with self.assertRaises(Exception):
            # openDSS has its own exception for this case
            circuit.add_load_nodes(params={"kV": -1})

        with self.assertRaises(ValueError):
            circuit.update_source(params={"kV": -1})

        # properly add load and source, then create invalid line
        with self.assertRaises(ValueError):
            circuit.add_lines([("source", "load0")], params={"length": -100})

    def test_103_invalid_nodes_in_line(self):
        circuit = PyGridSim()
        circuit.add_load_nodes()
        circuit.update_source()
        with self.assertRaises(KeyError):
            # only has source, load0 for now but tries to add another one
            circuit.add_lines([("source", "load5")])

    def test_104_non_int_parameters(self):
        circuit = PyGridSim()
        with self.assertRaises(TypeError):
            circuit.add_load_nodes(params={"kV": "stringInput"})

    def test_105_alt_source_parameters(self):
        circuit = PyGridSim()
        circuit.add_load_nodes(num=5)
        circuit.add_generators(params={"kV": 50, "kW": 100})
        circuit.add_PVSystems(load_nodes=["load0", "load1"], num_panels=5, params={"kV": 0.1})
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()

    def test_106_transformer_parameters(self):
        circuit = PyGridSim()
        circuit.add_load_nodes(num=5)
        circuit.update_source()
        circuit.add_lines([("source", "load0")], params={"length": 20, "XHL": 5})
        circuit.solve()
        print(circuit.results(["Voltages", "Losses"]))
        circuit.clear()


class TestTypeQueryFunctions(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        print("\nTest", self._testMethodName)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_200_type_queries(self):
        circuit = PyGridSim()
        # should still work if plural, capitalized, spaces
        for component in ["load ", "sources", "Line", "GENERATOR"]:
            print(circuit.get_types(component))
            print(circuit.get_types(component, show_ranges=True))

    def test_200_invalid_type_quer(self):
        circuit = PyGridSim()
        with self.assertRaises(KeyError):
            circuit.get_types("bad_component_name")
