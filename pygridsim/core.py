# -*- coding: utf-8 -*-
from altdss import altdss
from altdss import AltDSS, Transformer, Vsource, Load, LoadModel, LoadShape
from dss.enums import LineUnits, SolveModes
from parameters import make_load_node, make_source_node
from queries import query_solution
from lines import make_line
from enums import LineType, SourceType

"""Main module."""

class PyGridSim:
	def __init__(self):
		"""
		Initialize OpenDSS/AltDSS engine. Creates an Empty Circuit
		"""
		self.load_nodes = []
		self.num_loads = 0
		self.source_nodes = []
		self.num_sources = 0
		self.num_lines = 0
		altdss('new circuit.IEEE13Nodeckt')
	
	def add_load_nodes(self, load_params = {}, num = 1):
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
			load_nodes.append(make_load_node(load_params, self.num_loads))
			self.num_loads += 1
		self.load_nodes += load_nodes
		return load_nodes

	def add_source_nodes(self, source_params = {}, num = 1, source_type: SourceType = SourceType.TURBINE):
		"""
		When the user wants to manually add nodes, or make nodes with varying parameters.

		Args:
			source_params: load parameters for these manual additions
			lines: which nodes these new sources are connected to
			num (optional): number of sources to create with these parameters
		Return:
			List of source_nodes
		"""
		source_nodes = []
		for i in range(num):
			source_nodes.append(make_source_node(source_params, self.num_sources, source_type))
			self.num_sources += 1
		self.source_nodes += source_nodes
		return source_nodes
	
	def add_lines(self, connections, line_type: LineType = LineType.RESIDENTIAL_LV_LINE, params = {}):
		"""
		Specify all lines that the user wants to add. If redundant lines, doesn't add anything

		Args:
			connections: a list of new connections to add. Each item of the list follows the form (source1, load1)
			TODO: allow the input to also contain optional parameters
		"""
		for src, dst in connections:
			make_line(src, dst, line_type, self.num_lines, params)
			self.num_lines += 1


	def view_load_nodes(self, indices = []):
		"""
		View load nodes (what their parameters are) at the given indices.

		Args:
			indices (optional): Which indices to view the nodes at.
				If none given, display all
		"""
	

	def view_source_nodes(self, indices = []):
		"""
		View source nodes (what their parameters are) at the given indices.

		Args:
			indices (optional): Which indices to view the nodes at.
				If none given, display all
		"""
	

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