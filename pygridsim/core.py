# -*- coding: utf-8 -*-
from altdss import altdss

from pygridsim.configs import LOAD_CONFIGURATIONS
from pygridsim.enums import LoadType
from pygridsim.lines import _make_line
from pygridsim.parameters import _make_generator, _make_load_node, _make_pv, _make_source_node
from pygridsim.results import _export_results, _query_solution

"""Main module."""


class PyGridSim:
    def __init__(self):
        """Initialize OpenDSS engine.

        Instantiate an OpenDSS circuit that user can build circuit components on.
        Stores numbers of circuit components to ensure unique naming of repeat circuit components.

        Attributes:
            counts (dict[str, int]): Map of each type to the number seen of that type so far
        """
        self.counts = {}
        for count_type in ["loads", "lines", "transformers", "pv", "generators"]:
            self.counts[count_type] = 0

        altdss.ClearAll()
        altdss('new circuit.MyCircuit')

    def add_load_nodes(self,
                       load_type: str = "house",
                       params: dict[str, int] = None,
                       num: int = 1):
        """Adds Load Node(s) to circuit.

        Allows the user to add num load nodes,
        either with customized parameters or using a default load_type.

        Args:
            load_type (str, optional):
                Load type as a string, one of "house", "commercial", "industrial".
                Defaults to "house".
            params (dict[str, int], optional):
                Load parameters for these manual additions. Defaults to empty dictionary.
            num (int, optional):
                The number of loads to create with these parameters. Defaults to 1.

        Returns:
            list[OpenDSS object]:
                A list of OpenDSS objects representing the load nodes created.
        """

        params = params or dict()
        load_nodes = []
        for _ in range(num):
            _make_load_node(params, load_type, self.counts["loads"])
            self.counts["loads"] += 1

        return load_nodes

    def update_source(self, source_type: str = "turbine", params: dict[str, int] = None):
        """Adds or updates source node in system.

        If a Vsource node does not exist, it is created.
        Otherwise, its parameters are updated based on the provided values.

        Args:
            source_type (str, optional):
                The type of the source
                ("turbine", "powerplant", "lvsub", "mvsub", "hvsub", "shvsub").
                Defaults to "turbine".
            params (dict[str, int], optional):
                A dictionary of parameters to configure the source node. Defaults to None.

        Returns:
            OpenDSS object:
                The OpenDSS object representing the source node.
        """
        params = params or dict()
        return _make_source_node(params, source_type)

    def add_PVSystem(self,
                     load_nodes: list[str],
                     params: dict[str, int] = None,
                     num_panels: int = 1):
        """Adds a photovoltaic (PV) system to the specified load nodes.

        Adds PV system with num_panels to each of the listed load nodes.
        Can be customized with parameters.

        Args:
            load_nodes (list[str]):
                A list of node names where the PV system will be connected.
            params (dict[str, int], optional):
                A dictionary of additional parameters for the PV system. Defaults to None.
            num_panels (int, optional):
                The number of PV panels in the system. Defaults to 1.

        Returns:
            list[DSS objects]:
                A list of OpenDSS objects representing the PV systems created.
        """
        params = params or dict()
        if not load_nodes:
            raise ValueError("Need to enter load nodes to add PVSystem to")

        PV_nodes = []
        for load in load_nodes:
            PV_nodes.append(_make_pv(load, params, num_panels, self.counts["pv"]))
            self.counts["pv"] += 1

        return PV_nodes

    def add_generator(self, num: int = 1, gen_type: str = "small", params: dict[str, int] = None):
        """Adds generator(s) to the system.

        Args:
            num (int, optional):
                The number of generator units to add. Defaults to 1.
            gen_type (str, optional):
                The type of generator (one of "small", "large", "industrial"). Defaults to "small".
            params (dict[str, int], optional):
                A dictionary of parameters to configure the generator. Defaults to None.

        Returns:
            list[DSS objects]:
                A list of OpenDSS objects representing the generators created.
        """
        params = params or dict()
        generators = []
        for _ in range(num):
            generators.append(_make_generator(params, gen_type, count=self.counts["generators"]))
            self.counts["generators"] += 1

        return generators

    def add_lines(self,
                  connections: list[tuple],
                  line_type: str = "lv",
                  params: dict[str, int] = None,
                  transformer: bool = True):
        """Adds lines to the system.

        Adds electrical lines according to the given connections.
        Users can specify the parameters of the lines or otherwise use given line type options.

        Args:
            connections (list[tuple]):
                A list of tuples defining the connections between nodes.
            line_type (str, optional):
                The type of line (one of "lv", "mv", "hv"). Defaults to "lv".
            params (dict[str, int], optional):
                A dictionary of parameters to configure the lines. Defaults to None.
            transformer (bool, optional):
                Whether to include a transformer in the connection. Defaults to True.

        Returns:
            None
        """
        params = params or dict()
        for src, dst in connections:
            _make_line(src, dst, line_type, self.counts["lines"], params, transformer)
            self.counts["lines"] += 1

    def solve(self):
        """Solves the OpenDSS circuit.

        Initializes "solve" mode in OpenDSS, which allows user to query results on the circuit.

        Returns:
            None
        """
        altdss.Solution.Solve()

    def results(self, queries: list[str], export_path=""):
        """Gets simulation results based on specified queries.

        Allows the user to query for many results at once by providing a list of desired queries.

        Args:
            queries (list[str]):
                A list of queries to the circuit ("Voltages", "Losses", "TotalPower")
            export_path (str, optional):
                The file path to export results. If empty, results are not exported.
                Defaults to "".

        Returns:
            dict:
                A dictionary containing the fetched simulation results.
        """
        results = {}
        for query in queries:
            results[query] = _query_solution(query)

        if (export_path):
            _export_results(results, export_path)

        return results

    def clear(self):
        """Clears the OpenDSS circuit.

        Returns:
            None
        """
        altdss.ClearAll()
        for key in self.counts:
            self.counts[key] = 0

    def get_load_types(self, show_ranges: bool = False):
        """Provides list of all supported Load Types
    
        Args:
            show_ranges (bool, optional):
                Whether to show all configuration ranges in output.

        Returns:
            list:
                A list containing all load types, if show_ranges False.
                A list of tuples showing all load types and configurations, if show_ranges True.
        """
        if not show_ranges:
            return [load_type.value for load_type in LoadType]

        load_types = []
        for load_type in LoadType:
            config_dict = LOAD_CONFIGURATIONS[load_type]
            load_types.append((load_type.value, config_dict))

        return load_types
