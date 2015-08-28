"""@package bitcoin

This file contains class declaration of Transaction.
"""
import binaryRead
import Input
import Output
from helperfunc import converter

class Transaction:
	"""This class represents a Bitcoin transaction."""
	def __init__(self, blockNumber):
		"""Transaction constructor."""
		self.id = None
		self.blockNumber = blockNumber
		self.transactionVersion = None
		self.inputVarInt = None
		self.inputCount = None
		self.inputCountBinary = None
		self.inputList = []
		self.outputVarInt = None
		self.outputCount = None
		self.outputCountBinary = None
		self.outputList = []
		self.lockTime = None
		self.transactionHash = None

	def __str__(self):
		"""Object string representation."""
		string = ("Transaction Id: ", str(self.id),\
					"\nTransaction Hash: ", self.transactionHash,\
					"\nBlock Id: ", str(self.blockNumber),\
					"\nVersion: ", str(self.transactionVersion),\
					"\nInput Count: ", str(self.inputCount),\
					"\nOutput Count: ", str(self.outputCount),\
					"\nLocktime: ", str(self.lockTime))
		return ''.join(string)

	def setTransactionVersion(self, datFile):
		"""Sets transaction version."""
		self.transactionVersion = binaryRead.readUInt(datFile)

	def setInputVarInt(self, datFile):
		"""Sets input varint."""
		self.inputVarInt = binaryRead.readVarInt(datFile)

	def setInputCount(self, datFile):
		"""Sets input count."""
		countTupple = binaryRead.checkVariableLengthInteger(datFile, self.inputVarInt)
		self.inputCount = countTupple[0]
		self.inputCountBinary = countTupple[1]

	def setInputList(self, datFile):
		"""Sets input list."""
		for i in range(0, self.inputCount):
			input_ = Input.Input()
			input_.setInput(datFile)
			self.inputList.append(input_)

	def setOutputVarInt(self, datFile):
		"""Sets output varint."""
		self.outputVarInt = binaryRead.readVarInt(datFile)

	def setOutputCount(self, datFile):
		"""Sets output count."""
		countTupple = binaryRead.checkVariableLengthInteger(datFile, self.outputVarInt)
		self.outputCount = countTupple[0]
		self.outputCountBinary = countTupple[1]

	def setOutputList(self, datFile):
		"""Sets object output list."""
		for i in range(0, self.outputCount):
			output = Output.Output(i)
			output.setOutput(datFile)
			self.outputList.append(output)

	def setLockTime(self, datFile):
		"""Sets object locktime."""
		self.lockTime = binaryRead.readUInt(datFile)

	def setTransactionHash(self):
		"""Sets object transaction hash."""
		self.transactionHash = converter.transactionToTransactionHash(self.transactionVersion, \
																		self.inputVarInt, \
																		self.inputCountBinary, \
																		self.inputList, \
																		self.outputVarInt, \
																		self.outputCountBinary, \
																		self.outputList, \
																		self.lockTime)

	def setTransaction(self, datFile):
		"""Initializes Transaction from a .dat file."""
		self.setTransactionVersion(datFile)
		self.setInputVarInt(datFile)
		self.setInputCount(datFile)
		self.setInputList(datFile)
		self.setOutputVarInt(datFile)
		self.setOutputCount(datFile)
		self.setOutputList(datFile)
		self.setLockTime(datFile)
		self.setTransactionHash()

	def setTransactionFromDb(self, transactionRaw):
		"""Initializes Transaction from a database raw."""
		self.id = transactionRaw[0]
		self.transactionVersion = transactionRaw[2]
		self.inputCount = transactionRaw[3]
		self.outputCount = transactionRaw[4]
		self.lockTime = transactionRaw[5]
		self.transactionHash = transactionRaw[6]

	def toString(self):
		"""Humand readable print."""
		print "----------------------- TRANSACTION----------------------------"
		print "Transaction Version: " + binaryRead.uIntToStr(self.transactionVersion)
		print "Input Varint: " +  ''.join(str(self.inputVarInt).encode('hex'))
		print "Input Count: " + str(self.inputCount)
		for i in self.inputList:
			print i.toString()
		print "Output Varint: " +  ''.join(str(self.outputVarInt).encode('hex'))
		print "Output Count: " + str(self.outputCount)
		for i in self.outputList:
			print i.toString()
		print "Transaction LockTime: " + binaryRead.uIntToStr(self.lockTime)
		print "---------------------------------------------------------------"