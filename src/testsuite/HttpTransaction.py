"""@package testsuite

This file contains class declaration of HttpTransaction.
"""

import requests
import json

class HttpTransaction():
	"""This class fetches a Transaction of blockchain.info explorer.

	The main purpose of this class is to be used with the spelunkertest module.
	"""
	def __init__(self, transactionHash):
		"""HttpTransaction constructor.

		This method initializes the HttpTransaction from a transaction retrieved
		on blockchain.info.
		"""
		page = requests.get('https://blockchain.info/rawtx/' + transactionHash)
		self.transactionDict = json.loads(page.text)

	def __getitem__(self, arg):
		"""Dictionary style item getter.

		@param The name of the key retrieved.
		"""
		return self.transactionDict[arg]

	def toString(self):
		"""Human readable object printing."""
		for key in self.transactionDict:
			print "%s : %s" % (key, self.transactionDict[key])