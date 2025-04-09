# -*- coding: utf-8 -*-
from altdss import altdss
from pygridsim.parameters import _make_load_node, _make_source_node, _make_generator, _make_pv
from pygridsim.results import _query_solution, _export_results
from pygridsim.lines import _make_line

"""Main module."""

class PyGridSim:
	def __init__(self):
		"""Initialize OpenDSS engine.

		Instantiate an OpenDSS circuit that user can build circuit components on. Stores numbers of circuit components
		to ensure unique naming of repeat circuit components
		
		Attributes:
			num_loads (int): Number of loads in circuit so far.
			num_lines (int): Number of lines in circuit so far.
			num_transformers (int): Number of transformers in circuit so far.
			num_pv (int): Number of PV systems in circuit so far.
			num_generators (int): Number generators in circuit so far.
		"""
		self.num_loads = 0
		self.num_lines = 0
		self.num_transformers = 0
		self.num_pv = 0
		self.num_generators = 0
		altdss.ClearAll()
		altdss('new circuit.MyCircuit')
	
	def add_load_nodes(self, load_type: str = "house", params: dict[str, int] = None, num: int = 1):
		"""Adds Load Node(s) to circuit.
		
		Allows the user to add num load nodes, either with customized parameters or using a default load_type.

		Args: 
			load_type (str, optional):
				Load type as a string, one of "house", "commercial", "industrial". Defaults to "house".
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
			_make_load_node(params, load_type, self.num_loads)
			self.num_loads += 1

		return load_nodes

	def update_source(self, source_type: str = "turbine", params: dict[str, int] = None):
		"""Adds or updates source node in system.

		If a Vsource node does not exist, it is created. Otherwise, its parameters are updated based on the provided values.

		Args:
			source_type (str, optional):
				The type of the source (one of "turbine", "powerplant", "lvsub", "mvsub", "hvsub", "shvsub"). Defaults to "turbine".
        	params (dict[str, int], optional):
				A dictionary of parameters to configure the source node. Defaults to None.

		Returns:
			OpenDSS object:
				The OpenDSS object representing the source node.
		"""
		params = params or dict()
		return _make_source_node(params, source_type)

	def add_PVSystems(self, load_nodes: list[str], params: dict[str, int] = None, num_panels: int = 1):
		"""Adds a photovoltaic (PV) system to the specified load nodes.

		Adds PV system with num_panels to each of the listed load nodes. Can be customized with parameters.

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
			PV_nodes.append(_make_pv(load, params, num_panels, self.num_pv))
			self.num_pv += 1

		return PV_nodes
	
	def add_generators(self, num: int = 1, gen_type: str = "small", params: dict[str, int] = None):
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
			generators.append(_make_generator(params, gen_type, count=self.num_generators))
			self.num_generators += 1

		return generators
	

	def add_lines(self, connections: list[tuple], line_type: str = "lv", params: dict[str, int] = None, transformer: bool = True):
		"""Adds lines to the system.

		Adds electrical lines according to the given connections. Users can specify the parameters of the lines or otherwise use given line type options. 

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
			_make_line(src, dst, line_type, self.num_lines, params, transformer)
			self.num_lines += 1

	def solve(self):
		"""Solves the OpenDSS circuit.

		Initializes "solve" mode in OpenDSS, which then allows the user to query results on the circuit.

		Returns:
			None
		"""
		altdss.Solution.Solve()
	
	def results(self, queries: list[str], export_path = ""):
		"""Gets simulation results based on specified queries.
	
		Allows the user to query for many results at once by providing a list of desired queries.
		
		Args:
			queries (list[str]):  
				A list of queries to the circuit ("Voltages", "Losses", "TotalPower")
			export_path (str, optional):  
				The file path to export results. If empty, results are not exported. Defaults to "".  

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
		self.num_loads = 0
		self.num_lines = 0
		self.num_transformers = 0