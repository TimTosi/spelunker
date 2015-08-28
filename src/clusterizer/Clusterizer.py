"""@package clusterizer

This file contains class declaration of Clusterizer.
"""

class Clusterizer:
	"""This class aims to set up main chain, define orphan blocks and regroup addresses into clusters."""
	def __init__(self, db):
		"""Clusterizer constructor."""
		self.db = db

	def setBlocksHeigth(self):
		"""Updates the realNumber block attribute."""
		print "Setting Real Block Numbers (block height)..."
		currentBlock = self.db.getLastBlockByHeigth()
		if currentBlock != None:
			i = currentBlock.blockHeader.realNumber
		else:
			currentBlock = self.db.getBlockByNumber(0)
			i = 0
		lastBlock = self.db.getLastBlock()
		while currentBlock.blockHeader.blockHash != lastBlock.blockHeader.blockHash:
			print "Updating block %s as block %s" % (currentBlock.blockNumber, i)
			self.db.updateBlockHeigth(currentBlock.blockNumber, i)
			currentBlock = self.db.getBlockByHash(currentBlock.blockHeader.nextBlockHash)
			i += 1

	def setMainChain(self):
		"""Sets main chain blocks by updating the realNumber attribute."""
		print "Constructing Main Chain..."
		currentBlock = self.db.getLastMainChainBlock()
		if currentBlock == None:
			currentBlock = self.db.getLastBlock()
			self.db.updateOrphanState('blocks', currentBlock.blockNumber, False)
		while currentBlock.blockNumber != 0:
			print "Adding block %s in the Main Chain..." % currentBlock.blockNumber
			prevBlock = self.db.getBlockByHash(currentBlock.blockHeader.previousBlockHash)
			self.db.updateMainChain(prevBlock.blockNumber, currentBlock.blockHeader.blockHash)
			currentBlock = prevBlock
		print "Main Chain constructed."

	def setOrphanState(self):
		"""Updates orphan state of blocks."""
		print "Updating Orphan Blocks..."
		self.db.updateOrphanBlocks()
		self.setOrphanInputs()
		self.setOrphanOutputs()
		print "Orphan Blocks updated."

	def setOrphanInputs(self):
		"""Updates orphan state of inputs."""
		inputCount = self.db.getInputCount()
		state = self.db.getLastOrphanFlow('inputs')
		if state != None:
			for x in range(state, inputCount):
				print "Checking Orphan State of Input %s out of %s..." % (x, inputCount)
				block = self.db.getBlockByInputId(x)
				if block.blockHeader.isOphan == True:
					self.db.updateOrphanState('inputs', x, True)
				else:
					self.db.updateOrphanState('inputs', x, False)
		print "Orphan State of Input updated."

	def setOrphanOutputs(self):
		"""Updates orphan state of outputs."""
		outputCount = self.db.getOutputCount()
		state = self.db.getLastOrphanFlow('inputs')
		if state != None:
			for x in range(state, outputCount):
				print "Checking Orphan State of Output %s out of %s..." % (x, outputCount)
				block = self.db.getBlockByOutputId(x)
				if block.blockHeader.isOphan == True:
					self.db.updateOrphanState('outputs', x, True)
				else:
					self.db.updateOrphanState('outputs', x, False)
		print "Orphan State of Output updated."

	def setInputToLedger(self):
		"""Add inputs to the ledger table."""
		inputCount = self.db.getInputCount()
		for x in range(1, inputCount):
			print "Add Input %s out of %s to Ledger Table..." % (x, inputCount)
			input_ = self.db.getInputById(x)
			self.db.insertInputToLedger(input_)

	def setOutputToLedger(self):
		"""Add outputs to the ledger table."""
		outputCount = self.db.getOutputCount()
		for x in range(1, outputCount):
			print "Add Output %s out of %s to Ledger Table..." % (x, outputCount)
			output = self.db.getOutputById(x)
			self.db.insertOutputToLedger(output)

	def setLedger(self):
		"""Creates database indexes and call ledger creation functions."""
		print "Set Ledger Table..."
		print "Create Indexes..."
		self.db.createIndexes()
		print "Indexes created."
		self.setInputToLedger()
		self.setOutputToLedger()
		print "Ledger Table set."

	'''def regroupAddress(self):
		#transactionList = self.db.CHECKTRANSACTION with 2 outputs()
		for transaction in transactionList:
			if self.db.ALREADYSEEN(transaction.outputList[0].address) == False && self.db.ALREADYSEEN(transaction.outputList[1].address) == True
				self.db.AGGREGATE(transaction.input.ADDRESS, transaction.outputList[0].address)
			elif self.db.ALREADYSEEN(transaction.outputList[1].address) == False && self.db.ALREADYSEEN(transaction.outputList[0].address) == True
				self.db.AGGREGATE(transaction.input.ADDRESS, transaction.outputList[1].address)
		return'''

	def clusterize(self):
		"""Updates all database in order to create main chain, update block orphan state and regroup addresses into clusters."""
		self.setMainChain()
		self.setOrphanState()
		self.setBlocksHeigth()
		self.setLedger()
		#self.regroupAddress()