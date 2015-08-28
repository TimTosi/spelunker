"""@package bitcoin

This file contains class declaration of Block.
"""
import binaryRead
import BlockHeader
import Transaction

class Block:
	"""This class represents a Bitcoin block."""
	def __init__(self, datFile, blockNumber, fileName):
		"""Block constructor."""
		self.datFile = datFile
		self.blockNumber = blockNumber
		self.fileName = fileName
		self.blockHeader = None
		self.varInt = None
		self.transactionCount = None
		self.transactionList = []
		self.realSize = None

	def __str__(self):
		"""Object string representation."""
		string = ("Block Number: ", str(self.blockNumber),\
					"\nBlock Real Number: ", str(self.blockHeader.realNumber),\
					"\nBlock Hash: ", self.blockHeader.blockHash,\
					"\nMagic Id: ", self.blockHeader.magicID,\
					"\nLength: ", str(self.blockHeader.length),\
					"\nVersion: ", str(self.blockHeader.version),\
					"\nPrevious Block Hash: ", self.blockHeader.previousBlockHash,\
					"\nNext Block Hash: ", str(self.blockHeader.nextBlockHash),\
					"\nMerkle Root: ", self.blockHeader.merkleRoot,\
					"\nTarget Difficulty: ", str(self.blockHeader.targetDifficulty),\
					"\nNonce: ", str(self.blockHeader.nonce),\
					"\nOrphan: ", str(self.blockHeader.isOrphan),\
					"\nReal Size: ", str(self.realSize),\
					"\nFile Name: ", self.fileName,\
					"\nTimeStamp: ", self.blockHeader.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
		return ''.join(string)

	def setBlockHeader(self, blockHeader):
		"""Sets block header."""
		if blockHeader.setHeader() == False:
			return False
		self.blockHeader = blockHeader
		return True

	def setVarInt(self):
		"""Sets varint."""
		varInt = binaryRead.readVarInt(self.datFile)
		if varInt == False:
			return False
		self.varInt = varInt
		return True

	def setTransactionCount(self):
		"""Sets transaction count."""
		self.transactionCount = binaryRead.checkVariableLengthInteger(self.datFile, self.varInt)[0]

	def setTransactionList(self):
		"""Sets transaction list."""
		for i in range(0, self.transactionCount):
			transaction = Transaction.Transaction(self.blockNumber)
			transaction.setTransaction(self.datFile)
			self.transactionList.append(transaction)

	def setRealSize(self):
		"""Sets block real size."""
		self.realSize = binaryRead.offset
		binaryRead.offset = 0

	def setBlock(self):
		"""Sets Block from .dat file."""
		if self.setBlockHeader(BlockHeader.BlockHeader(self.datFile)) == False or self.setVarInt() == False:
			return False
		self.setTransactionCount()
		self.setTransactionList()
		self.setRealSize()
		return True

	def setBlockFromDb(self, rawBlock):
		"""Sets Block from a database raw."""
		self.realSize = rawBlock[10]
		self.blockHeader = BlockHeader.BlockHeader(None)
		self.blockHeader.setHeaderFromDb(rawBlock)

	def toString(self):
		"""Human readable print."""
		self.blockHeader.toString()
		print "Transaction Count: " + str(self.transactionCount)
		print "Varint : " +  ''.join(str(self.varInt).encode('hex'))
		print "Transaction Count: " + str(self.transactionCount)
		for i in self.transactionList:
			print i.toString()