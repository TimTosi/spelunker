"""@package testsuite

This file contains class declaration of HttpBlock.
"""

import requests
import json

class HttpBlock():
	"""This class fetches a Block of blockchain.info explorer.

	The main purpose of this class is to be used with the spelunkertest module.
	"""
	def __init__(self, blockHash):
		"""HttpBlock constructor.

		This method initializes the HttpBlock from a block retrieved
		on blockchain.info.
		"""
		page = requests.get('https://blockchain.info/rawblock/' + blockHash)
		self.blockDict = json.loads(page.text)

	def __getitem__(self, arg):
		"""Dictionary style item getter.

		@param arg The name of the key retrieved.
		@retval The value corresponding to the key provided.
		"""
		return self.blockDict[arg]

	def toString(self):
		"""Human readable object printing."""
		for key in self.blockDict:
			print "%s : %s" % (key, self.blockDict[key])