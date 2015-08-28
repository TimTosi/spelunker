"""@package bitcoin

This file contains class declaration of Blockheader.
"""
import binaryRead
from helperfunc import converter

class BlockHeader:
	"""This class represents a header of a Bitcoin block."""
	def __init__(self, datFile):
		"""BlockHeader constructor."""
		self.datFile = datFile
		self.magicID = None
		self.length = None
		self.version = None
		self.previousBlockHash = None
		self.merkleRoot = None
		self.timestamp = None
		self.targetDifficulty = None
		self.nonce = None
		self.blockHash = None
		self.realNumber = None
		self.isOrphan = None
		self.nextBlockHash = None

	def setMagicID(self):
		"""Sets magic ID."""
		intermediate = binaryRead.readByte(self.datFile)
		if not intermediate:
			self.magicID = False
			return
		elif intermediate == b'\x00':
			while intermediate == b'\x00':
				intermediate = binaryRead.readByte(self.datFile)
				if not intermediate:
					self.magicID = False
					return
		self.magicID = binaryRead.readMagicID(self.datFile, intermediate)

	def setBlockLength(self):
		"""Sets block length."""
		self.length = binaryRead.readUInt(self.datFile)

	def setVersion(self):
		"""Sets version."""
		self.version = binaryRead.readUInt(self.datFile)

	def setPreviousBlockHash(self):
		"""Sets previous block hash."""
		self.previousBlockHash = binaryRead.readHash(self.datFile)

	def setMerkleRoot(self):
		"""Sets merkle root."""
		self.merkleRoot = binaryRead.readHash(self.datFile)

	def setTimeStamp(self):
		"""Sets timestamp."""
		self.timestamp = binaryRead.readUInt(self.datFile)

	def setTargetDifficulty(self):
		"""Sets target difficulty."""
		self.targetDifficulty = binaryRead.readUInt(self.datFile)

	def setNonce(self):
		"""Sets nonce."""
		self.nonce = binaryRead.readUInt(self.datFile)

	def setBlockHash(self):
		"""Sets block hash."""
		self.blockHash = converter.blockHeaderToBlockHash(self.version, \
															self.previousBlockHash, \
															self.merkleRoot, \
															self.timestamp, \
															self.targetDifficulty, \
															self.nonce)

	def setHeader(self):
		"""Sets BlockHeader from .dat file."""
		self.setMagicID()
		if not self.magicID:
			return False
		self.setBlockLength()
		self.setVersion()
		self.setPreviousBlockHash()
		self.setMerkleRoot()
		self.setTimeStamp()
		self.setTargetDifficulty()
		self.setNonce()
		self.setBlockHash()
		return True

	def setHeaderFromDb(self, rawBlock):
		"""Sets BlockHeader from a database raw."""
		self.magicID = rawBlock[1]
		self.length = rawBlock[2]
		self.version = rawBlock[3]
		self.previousBlockHash = rawBlock[4]
		self.merkleRoot = rawBlock[5]
		self.targetDifficulty = rawBlock[6]
		self.nonce = rawBlock[7]
		self.blockHash = rawBlock[8]
		self.timestamp = rawBlock[11]
		self.realNumber = rawBlock[12]
		self.isOrphan = rawBlock[13]
		self.nextBlockHash =rawBlock[14]

	def toString(self):
		"""Human readable print."""
		print "###################BLOCK HEADER ###################"
		print "Magic ID: " + binaryRead.strToHex(self.magicID)
		print "Bloc Length: " + binaryRead.uIntToStr(self.length) + " bytes"
		print "Version: " + binaryRead.uIntToStr(self.version)
		print "Previous Block Hash: " + binaryRead.strToHex(self.previousBlockHash)
		print "Merkle Root: " + binaryRead.strToHex(self.merkleRoot)
		print "Time Stamp: " + binaryRead.binaryToTime(self.timestamp)
		print "Target Difficulty: " + binaryRead.strToHex(self.targetDifficulty)
		print "Nonce: " + binaryRead.uIntToStr(self.nonce)
		print "Block Hash: " + self.blockHash
		print "###################################################"