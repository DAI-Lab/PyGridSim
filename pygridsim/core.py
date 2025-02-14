# -*- coding: utf-8 -*-
from altdss import altdss
from altdss import AltDSS, Transformer, Vsource, Load, LoadModel, LoadShape
from dss.enums import LineUnits, SolveModes
from parameters import make_load_node, make_source_node
from queries import query_solution
from lines import make_line
from transformers import make_transformer
from enums import LineType, SourceType, LoadType

"""Main module."""

class PyGridSim:
	def __init__(self):
		"""
		Initialize OpenDSS/AltDSS engine. Creates an Empty Circuit
		"""
		self.num_loads = 0
		self.num_lines = 0
		self.num_transformers = 0
		altdss('new circuit.IEEE13Nodeckt')
	
	def add_load_nodes(self, load_params = {}, load_type: LoadType = LoadType.HOUSE, num = 1):
		"""
		When the user wants to manually add nodes, or make nodes with varying parameters.

		Args: 
			load_params: load parameters for these manual additions
			lines: which nodes these new loads are connected to
			num (optional): number of loads to create with these parameters
		Return:
			List of load_nodes
		"""
		load_nodes = []
		for i in range(num):
			make_load_node(load_params, load_type, self.num_loads)
			self.num_loads += 1
		return load_nodes

	def add_source_nodes(self, source_params = {}, source_type: SourceType = SourceType.TURBINE, num_in_batch = 1):
		"""
		When the user wants to manually add nodes, or make nodes with varying parameters.

		Args:
			source_params: load parameters for these manual additions
			lines: which nodes these new sources are connected to
			num (optional): number of sources to create with these parameters (removed for now)
			num_in_batch: how many to batch together directly (so they can't be connected to lines separately, etc.
				most common use case is if a house has 20 solar panels it's more useful to group them together)
		Return:
			List of source_nodes
		"""
		return make_source_node(source_params, source_type, num_in_batch=num_in_batch)

	def add_lines(self, connections, line_type: LineType = LineType.LV_LINE, params = {}):
		"""
		Specify all lines that the user wants to add. If redundant lines, doesn't add anything

		Args:
			connections: a list of new connections to add. Each item of the list follows the form (source1, load1)
			TODO: allow the input to also contain optional parameters
		"""
		for src, dst in connections:
			make_line(src, dst, line_type, self.num_lines, params)
			self.num_lines += 1

	def add_transformers(self, connections, params = {}):
		"""
		Specify all transformers that the user wants to add, same input style as lines.

		Args:
			connections: a list of new transformers to add (where to add them), with these params
		"""
		for src, dst in connections:
			make_transformer(src, dst, self.num_transformers, params)
			self.num_transformers += 1


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
		"""
		altdss.Solution.Solve()
	
	def results(self, queries):
		"""
		Allow the user to query for many results at once instead of learning how to manually query

		Returns:
			Results for each query, in a dictionary
		"""
		results = {}
		for query in queries:
			results[query] = query_solution(query)
		return results

	def remove_load_nodes(self, indices):
		"""
		All load nodes are defined by indices, so remove the ones in list of indices.

		Args:
			indices: indices corresponding to nodes to remove (i.e. [1,3] removes the 1st and 3rd load nodes)
		"""

	def remove_source_nodes(self, indices):
		"""
		All source nodes are defined by indices, so remove the ones in list of indices
	
		Args:
			indices: indices corresponding to nodes to remove
		"""

	def remove_lines(self, connections):
		"""
		Remove all the connections (and any corresponding transformers) specified.

		Args:
			connections: a list of connections to remove
		"""