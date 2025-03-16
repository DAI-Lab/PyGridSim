# -*- coding: utf-8 -*-
from altdss import altdss
from altdss import AltDSS, Transformer, Vsource, Load, LoadModel, LoadShape
from dss.enums import LineUnits, SolveModes
from pygridsim.parameters import *
from pygridsim.results import query_solution, export_results
from pygridsim.lines import make_line
from pygridsim.transformers import make_transformer
from pygridsim.enums import LineType, SourceType, LoadType, GeneratorType

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
	
	def add_load_nodes(self, params = {}, load_type: LoadType = LoadType.HOUSE, num = 1):
		"""
		When the user wants to manually add nodes, or make nodes with varying parameters.

		Args: 
			params: load parameters for these manual additions
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

	def update_source(self, params = {}, source_type: SourceType = SourceType.TURBINE):
		"""
		Adds a main voltage source if it doesn't exist, otherwise edits it

		Args:
			params: load parameters for these manual additions
			lines: which nodes these new sources are connected to
			num (optional): number of sources to create with these parameters (removed for now)
			(removed) num_in_batch: how many to batch together directly (so they can't be connected to lines separately, etc.
				most common use case is if a house has 20 solar panels it's more useful to group them together)
		Return:
			List of source_nodes
		"""
		return make_source_node(params, source_type)

	def add_PVSystem(self, load_nodes, params = {}, num_panels = 1):
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
	
	def add_generator(self, num, params = {}, gen_type: GeneratorType = GeneratorType.SMALL):
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
	

	def add_lines(self, connections, line_type: LineType = LineType.LV_LINE, params = {}, transformer = True):
		"""
		Specify all lines that the user wants to add. If redundant lines, doesn't add anything

		Args:
			connections: a list of new connections to add. Each item of the list follows the form (source1, load1)
			TODO: allow the input to also contain optional parameters
		"""
		for src, dst in connections:
			make_line(src, dst, line_type, self.num_lines, params, transformer)
			self.num_lines += 1

	def view_load_nodes(self, indices = []):
		"""
		View load nodes (what their parameters are) at the given indices.

		Args:
			indices (optional): Which indices to view the nodes at.
				If none given, display all
		"""
		load_nodes = []
		if not indices:
			indices = [i for i in range(self.num_loads)]
		
		for idx in indices:
			load_obj = altdss.Load["load" + str(idx)]
			load_info = {}
			load_info["name"] = "load" + str(idx)
			load_info["kV"] = load_obj.kV
			load_info["kW"] = load_obj.kW
			load_info["kVar"] = load_obj.kvar
			load_nodes.append(load_info)
		return load_nodes
	

	def view_source_node(self):
		"""
		View source nodes (what their parameters are) at the given indices.

		Args:
			indices (optional): Which indices to view the nodes at.
				If none given, display all
		
		TODO once capability for more source nodes is initialized
		"""
		source_obj = altdss.Vsource["source"]
		source_info = {}
		source_info["name"] = "source"
		source_info["kV"] = source_obj.BasekV
		return source_info

	def solve(self):
		"""
		Initialize "solve" mode in AltDSS, then allowing the user to query various results on the circuit

		TODO: error handling here
		"""
		altdss.Solution.Solve()
	
	def results(self, queries, export_path = ""):
		"""
		Allow the user to query for many results at once instead of learning how to manually query

		Returns:
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
		TODO: maybe this isn't necessary because it's done in the beginning
		"""
		altdss.ClearAll()
		self.num_loads = 0
		self.num_lines = 0
		self.num_transformers = 0