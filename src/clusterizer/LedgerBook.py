"""@package clusterizer

This file contains class declaration of LedgerBook.
"""

class LedgerBook:
	"""This class represents a Bitcoin wallet."""
	def __init__(self):
		"""LedgerBook constructor"""
		self.ledgerLineList = []

	def append(self, item):
		"""Appends a LedgerLine to the object."""
		self.ledgerLineList.append(item)

	def __getitem__(self, key):
		"""Dictionary style item getter.

		@param arg The name of the key retrieved.
		@retval The value corresponding to the key provided.
		"""
		return self.ledgerList[key]

	def getLedgerSum(self):
		"""Computes currency detained from all ledgerLines."""
		finalSum = 0
		for ledgerLine in self.ledgerLineList:
			if ledgerLine.operation == True:
				finalSum += ledgerLine.value
			else:
				finalSum -= ledgerLine.value
		return finalSum