"""@package clusterizer

This file contains class declaration of LedgerLine.
"""

class LedgerLine:
	"""This class represents a raw in the Ledger table."""
	def __init__(self):
		"""LedgerLine constructor."""
		self.Id = None
		self.address = None
		self.operation = None
		self.value = None
		self.timestamp = None

	def __str__(self):
		"""Object printable representation."""
		string = ("Id: ", str(self.id),\
					"\nAddress: ", self.address,\
					"\nOperation: ", str(self.operation),\
					"\nValue: ", str(self.value),\
					"\nTimeStamp: ", self.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
		return ''.join(string)

	def setId(self, Id):
		"""Sets object ID."""
		self.Id = Id

	def setAddress(self, address):
		"""Sets object address."""
		self.address = address

	def setOperation(self, operation):
		"""Sets object operation."""
		self.operation = operation

	def setValue(self, value):
		"""Sets object value."""
		self.value = value

	def setTimestamp(self, timestamp):
		"""Sets object timestamp."""
		self.timestamp = timestamp

	def setLedgerLineFromDb(self, rawLedgerLine):
		"""Sets all object attributes."""
		self.setId(rawLedgerLine[0])
		self.setAddress(rawLedgerLine[1])
		self.setOperation(rawLedgerLine[2])
		self.setValue(rawLedgerLine[3])
		self.setTimestamp(rawLedgerLine[4])