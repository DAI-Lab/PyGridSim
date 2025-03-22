# -*- coding: utf-8 -*-
from altdss import altdss
from pygridsim.parameters import make_load_node, make_source_node, make_generator, make_pv
from pygridsim.results import query_solution, export_results
from pygridsim.lines import make_line

"""Main module."""

class PyGridSim:
	def __init__(self):
		"""
		Initialize OpenDSS/AltDSS engine. Creates an Empty Circuit
		"""
		self.num_loads = 0
		self.num_lines = 0
		self.num_transformers = 0
		self.num_pv = 0
		self.num_generators = 0
		altdss.ClearAll()
		altdss('new circuit.MyCircuit')
	
	def add_load_nodes(self, load_type: str = "house", params = {}, num: int = 1):
		"""
		When the user wants to manually add nodes, or make nodes with varying parameters.

		Args: 
			params: load parameters for these manual additions
			load_type: input as string, representing one of the load types
			lines: which nodes these new loads are connected to
			num (optional): number of loads to create with these parameters
		Return:
			List of load_nodes
		"""
		load_nodes = []
		for _ in range(num):
			make_load_node(params, load_type, self.num_loads)
			self.num_loads += 1
		return load_nodes

	def update_source(self, source_type: str = "turbine", params = {}):
		"""
		Adds a main voltage source if it doesn't exist, otherwise edits it

		Args:
			source_type: source type as a string
			params: load parameters for these manual additions
		Return:
			List of source_nodes
		"""
		return make_source_node(params, source_type)

	def add_PVSystem(self, load_nodes: list[str], params = {}, num_panels: int = 1):
		"""
		Specify a list of load nodes to add a PVsystem ("solar panel") to.

		Args:
		    load_nodes: which load nodes to add PVsystem to
			params: specify anything else about the PVsystem. otherwise defaults to typical solar panel
			num_panels: representing how many solar panels (to represent scale)
		Return:
			list of PVSystem objects
		"""
		if not load_nodes:
			raise ValueError("Need to enter load nodes to add PVSystem to")
		PV_nodes = []
		for load in load_nodes:
			PV_nodes.append(make_pv(load, params, num_panels, self.num_pv))
			self.num_pv += 1
		return PV_nodes
	
	def add_generator(self, num: int = 1, gen_type: str = "small", params = {}):
		"""
		Specify parameters for a generator to add to the circuit

		Args:
			num: number of generators
			gen_type: specify the generator type (small, large, industrial)
			params: specify anything else about the generator.
		Return:
			list of generator objects
		"""
		generators = []
		for _ in range(num):
			generators.append(make_generator(params, gen_type, count=self.num_generators))
			self.num_generators += 1
		return generators
	

	def add_lines(self, connections: list[tuple], line_type: str = "lv", params = {}, transformer: bool = True):
		"""
		Specify all lines that the user wants to add. If redundant lines, doesn't add anything

		Args:
			connections: a list of new connections to add. Each item of the list follows the form (source1, load1)
			line_type: a string representing linetype if user wants to use preset parameters
			params: any custom parameters for lines or transformers
			transformer: whether or not to include a transformer, default yes
		"""
		for src, dst in connections:
			make_line(src, dst, line_type, self.num_lines, params, transformer)
			self.num_lines += 1

	def solve(self):
		"""
		Initialize "solve" mode in AltDSS, then allowing the user to query various results on the circuit
		"""
		altdss.Solution.Solve()
	
	def results(self, queries: list[str], export_path = ""):
		"""
		Allow the user to query for many results at once instead of learning how to manually query
		
		Args:
			queries: List of queries to fetch the result of
			export_path: if specified, exports result to this string
		Return:
			Results for each query, in a dictionary
		"""
		results = {}
		for query in queries:
			results[query] = query_solution(query)
		if (export_path):
			export_results(results, export_path)
		return results
	
	def clear(self):
		"""
		Must call after we are done using the circuit, or will cause re-creation errors.

		We only work with one circuit at a time, can only have one PyGridSim object at a time.
		"""
		altdss.ClearAll()
		self.num_loads = 0
		self.num_lines = 0
		self.num_transformers = 0