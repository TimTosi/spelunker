"""@package bitcoin

This file contains class declaration of Input.
"""
import binaryRead

class Input:
	"""This class represents a Bitcoin input."""
	def __init__(self):
		"""Input constructor."""
		self.id = None
		self.transactionId = None
		self.transactionHash = None
		self.transactionIndex = None
		self.varInt = None
		self.scriptLength = None
		self.scriptLengthBinary = None
		self.scriptData = None
		self.isCoinbase = None
		self.sequenceNumber = None
		self.isOrphan = None

	def __str__(self):
		"""Object string representation."""
		string = ("Id: ", str(self.id),\
					"\nTransaction Id: ", str(self.transactionId),\
					"\nTransaction Hash: ", self.transactionHash,\
					"\nTransaction Index: ", str(self.transactionIndex),\
					"\nCoinbase: ", str(self.isCoinbase),\
					"\nSequence Number: ", str(self.sequenceNumber),\
					"\nScript Data: ", self.scriptData)
		return ''.join(string)

	def setTransactionHash(self, datFile):
		"""Sets transaction hash."""
		self.transactionHash = binaryRead.readHash(datFile)

	def setTransactionIndex(self, datFile):
		"""Sets transaction index."""
		self.transactionIndex = binaryRead.readUInt(datFile)

	def setVarInt(self, datFile):
		"""Sets varint."""
		self.varInt = binaryRead.readVarInt(datFile)

	def setScriptLength(self, datFile, varInt):
		"""Sets script length."""
		lengthTupple = binaryRead.checkVariableLengthInteger(datFile, varInt)
		self.scriptLength = lengthTupple[0]
		self.scriptLengthBinary = lengthTupple[1]

	def setScriptData(self, datFile, scriptLength):
		"""Sets input script."""
		self.scriptData = binaryRead.readByteNumber(datFile, scriptLength)

	def setCoinbase(self, transactionHash):
		"""Sets coinbase state."""
		coinbaseCode = binaryRead.uIntToStr(transactionHash)
		if (coinbaseCode == '4294967295'):
			self.isCoinbase = True
		else:
			self.isCoinbase = False

	def setSequenceNumber(self, datFile):
		"""Sets sequence number."""
		self.sequenceNumber = binaryRead.readUInt(datFile)

	def setInput(self, datFile):
		"""Sets Input from .dat file."""
		self.setTransactionHash(datFile)
		self.setTransactionIndex(datFile)
		self.setVarInt(datFile)
		self.setScriptLength(datFile, self.varInt)
		self.setScriptData(datFile, self.scriptLength)
		self.setCoinbase(self.transactionIndex)
		self.setSequenceNumber(datFile)

	def setInputFromDb(self, rawInput):
		"""Sets Input from a database raw."""
		self.id = rawInput[0]
		self.transactionId = rawInput[1]
		self.transactionHash = rawInput[2]
		self.transactionIndex = rawInput[3]
		self.isCoinbase = rawInput[4]
		self.sequenceNumber = rawInput[5]
		self.scriptData = rawInput[6]
		self.isOrphan = rawInput[7]


	def toString(self):
		"""Human readable print."""
		print "@@@@@@@@@@@@@@@@@@@@@@@ INPUT @@@@@@@@@@@@@@@@@@@@@@@@@@@"
		print "Transaction Hash: " + binaryRead.strToHex(self.transactionHash)
		print "Transaction Index: " + binaryRead.uIntToStr(self.transactionIndex)
		print "Varint: " + ''.join(str(self.varInt).encode('hex'))
		print "Script Length: " + str(self.scriptLength)
		print "Script Data Encoded: " + binaryRead.strToHex(self.scriptData)
		print "Script Data Decoded: " + self.scriptData
		print "Coinbase: " + str(self.isCoinbase)
		print "Sequence Number: " + binaryRead.uIntToStr(self.sequenceNumber)
		print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"