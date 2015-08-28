"""@package clusterizer

This file contains class declaration of Address.
"""

class Address:
	"""This class represents a Bitcoin address."""
	def __init__(self, id_, clusterId):
		"""Address constructor."""
		self.id = id_
		self.clusterId = clusterId

	def setId(self, id_):
		"""Sets object ID."""
		self.id = id_

	def setClusterId(self, clusterId):
		"""Sets object cluster ID."""
		self.clusterId = clusterId