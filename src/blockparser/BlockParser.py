"""@package blockparser

This file contains class declaration of Blockparser.
"""
import sys
import bitcoin.Block as BTBlock
import bitcoin.binaryRead as binaryRead

class BlockParser:
	"""This class helps to parse .dat files to format datas."""
	def __init__(self, db, settings):
		"""Blockparser constructor."""
		self.db = db
		self.blockCount = 0
		self.dirList = settings["dirList"]
		self.lastOffset = None

	def setDatFileList(self, lastDatFile):
		"""Sets the list of all files to parse."""
		i = 0
		while self.dirList[i] != lastDatFile:
			i = i + 1
		self.dirList = self.dirList[i:]

	def configureLastEnv(self, lastBlock):
		"""Updates configuration to continue parsing from the last state."""
		self.lastOffset = self.db.getLastOffset(lastBlock.fileName)
		self.setDatFileList(lastBlock.fileName)
		self.blockCount = lastBlock.blockNumber + 1

	def parseDatFile(self, datFile, fileName):
		"""Parses a .dat file."""
		while True:
			print "Processing Block %d ..." % self.blockCount
			blockExtracted = BTBlock.Block(datFile, self.blockCount, fileName)
			if blockExtracted.setBlock() == False:
				return
			self.db.insertFullBlock(blockExtracted)
			self.blockCount += 1

	def parseFromLastBlock(self):
		"""Parses files from the last block parsed."""
		with open(self.dirList[0], 'rb') as datFile:
			binaryRead.readByteNumber(datFile, self.lastOffset)
			binaryRead.offset = 0
			print "Processing File %s ..." % self.dirList[0]
			self.parseDatFile(datFile, self.dirList[0])
			print "The parsing of the file %s is done." % self.dirList[0]
			self.dirList = self.dirList[1:]
		self.parseFromFirstBlock()

	def parseFromFirstBlock(self):
		"""Parses data from the first block."""
		for datFileName in self.dirList:
			print "Processing File %s ..." % datFileName
			with open(datFileName, 'rb') as datFile:
				self.parseDatFile(datFile, datFileName)
				print "The parsing of the file %s is done." % datFileName

	def parse(self):
		"""Sets last configuration or new parsing phase."""
		lastBlock = self.db.getLastBlock()
		if lastBlock == None:
			self.parseFromFirstBlock()
		else:
			self.configureLastEnv(lastBlock)
			self.parseFromLastBlock()
		print "End Of Parsing"
