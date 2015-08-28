"""@package postgreDb
Database manager / wrapper.

This module provides a proxy object in order to interract
with a postres database. Uses psycopg2 module.
"""

import psycopg2
import formatedQueries
from bitcoin import binaryRead
from bitcoin import Block
from bitcoin import Transaction
from bitcoin import Input
from bitcoin import Output
from clusterizer import LedgerBook
from clusterizer import LedgerLine

class DatabaseWrapper:
	"""Database manager class.

	This class provides several useful functions used by the parser
	and the clusterizer for inserting and retrieving datas.
	"""
	def __init__(self, dbCredentials):
		"""DatabaseWrapper constructor.

		This method initializes the DatabaseWrapper with conf.ini settings.
		"""
		self.dbCredentials = dbCredentials
		self.dbConnection = None
		self.cursor = None
		self.query = None
		self.result = None
		self.lastId = None

#-------INITIALIZATION FUNCTIONS

	def setDatabaseEnv(self):
		"""Initializes database connector and creates tables."""
		self.connect(self.dbCredentials)
		self.createDatabaseTables()

#-------BASIC WRAPPER FUNCTIONS

	def connect(self, dbCredentials):
		"""Establishes database connection.

		@param dbCredentials String containing username, password and database name for connection.
		"""
		self.dbConnection = psycopg2.connect(dbCredentials)
		self.cursor = self.dbConnection.cursor()

	def close(self):
		"""Closes database connection"""
		self.dbConnection.close()

	def commit(self):
		"""Commits changes in the database."""
		self.dbConnection.commit()

	def setLastId(self):
		"""Sets the id of the last row inserted into the object."""
		self.lastId = self.cursor.fetchone()[0]

	def prepareQuery(self, query):
		"""Sets a query into the object for later use.

		@param query String containing the query.
		"""
		self.query = query

	def executeQueryFetch(self, query = None):
		"""Executes the query passed in parameter and returns the result.

		If no query is passed in parameter, uses the last query set.
		@param query String containing the query to execute.
		@retval self.result The result of the query.
		"""
		if query == None:
			query = self.query
		self.cursor.execute(query)
		self.result = self.cursor.fetchall()
		return self.result

	def executeQuery(self, query = None, args = None):
		"""Executes the query passed in parameter with args value.

		If no query is passed in parameter, uses the last query set.
		Can be used without args.
		@param query String containing the query to execute.
		@param args Tupple of arguments to use with the query.
		"""
		if query == None:
			query = self.query
		if args != None:
			self.cursor.execute(query, args)
		else:
			self.cursor.execute(query)

	def fetchOne(self):
		"""Fetches the first result of the last query executed.

		@retval self.result The result of the last query executed"""
		self.result = self.cursor.fetchone()
		return self.result

	def fetchAll(self):
		"""Fetches the result of the last query executed.

		@retval self.result The result of the last query executed"""
		self.result = self.cursor.fetchall()
		return self.result

#-------GET OBJECTS

	def getBlockByNumber(self, blockNumber):
		"""Retrieves a block from the database from its ID and initializes it.

		@param blockNumber The block ID.
		@retval block Block object.
		"""
		query = 'SELECT * from blocks where id = %s'
		self.executeQuery(query, (blockNumber,))
		rawBlock = self.fetchOne()
		block = Block.Block(None, rawBlock[0], rawBlock[9])
		block.setBlockFromDb(rawBlock)
		return block

	def getBlockByHeigth(self, heigth):
		"""Retrieves a block from the database from its heigth and initializes it.

		@param heigth The block heigth.
		@retval block Block object.
		"""
		query = 'SELECT * from blocks where real_number = %s'
		self.executeQuery(query, (heigth,))
		rawBlock = self.fetchOne()
		block = Block.Block(None, rawBlock[0], rawBlock[9])
		block.setBlockFromDb(rawBlock)
		return block

	def getBlockByHash(self, blockHash):
		"""Retrieves a block from the database from its hash and initializes it.

		@param blockHash The hash value of the block.
		@retval block Block object.
		"""
		query = 'SELECT * from blocks where block_hash = %s'
		self.executeQuery(query, (blockHash,))
		rawBlock = self.fetchOne()
		block = Block.Block(None, rawBlock[0], rawBlock[9])
		block.setBlockFromDb(rawBlock)
		return block

	def getBlockByTxId(self, transactionId):
		"""Retrieves a block from the database from a transaction ID and initializes it.

		@param transactionId The ID of the transaction used to retrieve the block.
		@retval self.getBlockByNumber(rawTransaction[1]) Call to getBlockByNumber method.
		"""
		query = 'SELECT * from transactions where id = %s'
		self.executeQuery(query, (transactionId,))
		rawTransaction = self.fetchOne()
		return self.getBlockByNumber(rawTransaction[1])

	def getBlockByInputId(self, inputId):
		"""Retrieves a block from the database from an input ID and initializes it.

		@param inputId The ID of the input used to retrieve the block.
		@retval self.getBlockByTxId(rawInput[1]) Call to getBlockByTxId method.
		"""
		query = 'SELECT * from inputs where id = %s'
		self.executeQuery(query, (inputId,))
		rawInput = self.fetchOne()
		return self.getBlockByTxId(rawInput[1])

	def getBlockByOutputId(self, outputId):
		"""Retrieves a block from the database from an output ID and initializes it.

		@param outputId The ID of the output used to retrieve the block.
		@retval self.getBlockByTxId(rawOutput[1]) Call to getBlockByTxId method.
		"""
		query = 'SELECT * from outputs where id = %s'
		self.executeQuery(query, (outputId,))
		rawOutput = self.fetchOne()
		return self.getBlockByTxId(rawOutput[1])

	def getLastBlock(self):
		"""Retrieves the last block inserted into the database.

		@retval block Block object.
		"""
		query = 'SELECT * from blocks ORDER BY id DESC LIMIT 1'
		self.executeQuery(query)
		rawBlock = self.fetchOne()
		if rawBlock == None:
			return None
		block = Block.Block(None, rawBlock[0], rawBlock[9])
		block.setBlockFromDb(rawBlock)
		return block

	def getTxById(self, id_):
		"""Retrieves a transaction from the database from its ID and initializes it.

		@param id_ The ID of the transaction.
		@retval Transaction object.
		"""
		query = 'SELECT * from transactions where id = %s'
		self.executeQuery(query, (id_,))
		rawTransaction = self.fetchOne()
		transaction = Transaction.Transaction(rawTransaction[1])
		transaction.setTransactionFromDb(rawTransaction)
		return transaction

	def getTxByBlockNumber(self, blockNumber):
		"""Retrieves the list of transactions from the database corresponding to
		a block ID and initializes them.

		@param blockNumber The block ID.
		@retval transactionList The list of Transaction objects.
		"""
		query = 'SELECT * from transactions where block_id = %s'
		self.executeQuery(query, (blockNumber,))
		rawTransactionList = self.fetchAll()
		transactionList = []
		for rawTransaction in rawTransactionList:
			transaction = Transaction.Transaction(rawTransaction[1])
			transaction.setTransactionFromDb(rawTransaction)
			transactionList.append(transaction)
		return transactionList

	def getInputById(self, id_):
		"""Retrieves an input from the database from its ID and initializes it.

		@param id_ The input ID.
		@retval input_ Input object.
		"""
		query = 'SELECT * from inputs where id = %s'
		self.executeQuery(query, (id_,))
		rawInput = self.fetchOne()
		input_ = Input.Input()
		input_.setInputFromDb(rawInput)
		return input_

	def getOutputById(self, id_):
		"""Retrieves an output from the database from its ID and initializes it.

		@param id_ The output ID.
		@retval output Output object.
		"""
		query = 'SELECT * from outputs where id = %s'
		self.executeQuery(query, (id_,))
		rawOutput = self.fetchOne()
		output = Output.Output()
		output.setInputFromDb(rawOutput)
		return output

	def getInputByTxId(self, transactionId):
		"""Retrieves a list of input from the database corresponding to a transaction ID and initializes them.

		@param transactionId The transaction ID.
		@retval inputList The list of Input objects.
		"""
		query = 'SELECT * from inputs where transaction_id = %s'
		self.executeQuery(query, (transactionId,))
		rawInputList = self.fetchAll()
		inputList = []
		for rawInput in rawInputList:
			input_ = Input.Input()
			input_.setInputFromDb(rawInput)
			inputList.append(input_)
		return inputList

	def getOutputByTxId(self, transactionId):
		"""Retrieves a list of output from the database corresponding to a transaction ID and initializes them.

		@param transactionId The transaction ID.
		@retval outputList The list of Output objects.
		"""
		query = 'SELECT * from outputs where transaction_id = %s'
		self.executeQuery(query, (transactionId,))
		outputRawList = self.fetchAll()
		outputList = []
		for outputRaw in outputRawList:
			output = Output.Output(outputRaw[5])
			output.setOutputFromDb(outputRaw)
			outputList.append(output)
		return outputList

	def getFullBlockByNumber(self, blockNumber):
		"""Retrieves a block from the database from its ID and initializes it.

		Sets all Transaction, Input and Output objects corresponding to the block.
		@param blockNumber The block ID.
		@retval block Block object.
		"""
		query = 'SELECT * from blocks where id = %s'
		self.executeQuery(query, (blockNumber,))
		rawBlock = self.fetchOne()
		block = Block.Block(None, rawBlock[0], rawBlock[9])
		block.setBlockFromDb(rawBlock)
		block.transactionList = self.getFullTxByBlockNumber(blockNumber)
		return block

	def getFullTxByBlockNumber(self, blockNumber):
		"""Retrieves a list of transactions from the database corresponding to a block ID and initializes them.

		Sets all Input and Output objects corresponding to each Transaction.
		@param blockNumber The block ID.
		@retval transaction The list of Transaction objects.
		"""
		query = 'SELECT * from transactions where block_id = %s'
		self.executeQuery(query, (blockNumber,))
		transactionRawList = self.fetchAll()
		transactionList = []
		for transactionRaw in transactionRawList:
			transaction = Transaction.Transaction(transactionRaw[1])
			transaction.setTransactionFromDb(transactionRaw)
			transaction.inputList = self.getInputByTxId(transaction.id)
			transaction.outputList = self.getOutputByTxId(transaction.id)
			transactionList.append(transaction)
		return transactionList

	def getPreviousOutputFromInput(self, input_):
		"""Retrieves an Output from the database corresponding to its future Input and initializes it.

		@param input_ Input object.
		@retval output Output object.
		"""
		query = 'SELECT * from transactions where transaction_hash = %s'
		self.executeQuery(query, (input_.transactionHash,))
		rawTransaction = self.fetchOne()
		if rawTransaction == None:
			return None
		query = 'SELECT * from outputs where transaction_id = %s and index = %s'
		self.executeQuery(query, (rawTransaction[0], input_.transactionIndex))
		outputRaw = self.fetchOne()
		output = Output.Output(outputRaw[5])
		output.setOutputFromDb(outputRaw)
		return output

#-------INSERT OBJECTS

	def insertFullBlock(self, block):
		"""Inserts a block and its related transactions, inputs and outputs into the database.

		@param block Block object.
		"""
		self.insertBlock(block)
		for transaction in block.transactionList:
			self.insertTransaction(transaction)
			for input_ in transaction.inputList:
				self.insertInput(input_)
			for output in transaction.outputList:
				self.insertOutput(output)
		self.commit()

	def insertBlock(self, block):
		"""Inserts a block into the database.

		Does not commit database modification.
		@param block Block object.
		"""
		query = '	INSERT INTO blocks (id, magic_id, length, version, previous_block_hash, merkle_root, target_difficulty, nonce, block_hash, file_name, real_size, block_timestamp) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		self.executeQuery(query, (\
					str(block.blockNumber), \
					binaryRead.strToHex(block.blockHeader.magicID), \
					binaryRead.uIntToStr(block.blockHeader.length), \
					binaryRead.uIntToStr(block.blockHeader.version), \
					binaryRead.strToHex(block.blockHeader.previousBlockHash), \
					binaryRead.strToHex(block.blockHeader.merkleRoot), \
					binaryRead.uIntToStr(block.blockHeader.targetDifficulty), \
					binaryRead.uIntToStr(block.blockHeader.nonce), \
					block.blockHeader.blockHash, \
					block.fileName, \
					block.realSize, \
					binaryRead.binaryToTime(block.blockHeader.timestamp)))

	def insertTransaction(self, transaction):
		"""Inserts a transaction into the database.

		Does not commit database modification.
		Sets lastId attribute of DatabaseWrapper to the value of the inserted transaction ID.
		@param transaction Transaction object.
		"""
		query = '	INSERT INTO transactions (block_id, version, input_count, output_count, locktime, transaction_hash) \
					VALUES (%s, %s, %s, %s, %s, %s) RETURNING id'
		self.executeQuery(query, (\
					str(transaction.blockNumber), \
					binaryRead.uIntToStr(transaction.transactionVersion), \
					str(transaction.inputCount), \
					str(transaction.outputCount), \
					binaryRead.uIntToStr(transaction.lockTime), \
					transaction.transactionHash))
		self.setLastId()

	def insertInput(self, input_):
		"""Inserts an input into the database.

		Does not commit database modification.
		@param input_ Input object.
		"""
		query = '	INSERT INTO inputs (transaction_id, transaction_hash, transaction_index, coinbase, sequence_number, script) \
					VALUES (%s, %s, %s, %s, %s, %s)'
		self.executeQuery(query, (\
					self.lastId, \
					binaryRead.strToHex(input_.transactionHash), \
					binaryRead.uIntToStr(input_.transactionIndex), \
					input_.isCoinbase, \
					binaryRead.uIntToStr(input_.sequenceNumber), \
					binaryRead.strToHex(input_.scriptData)))

	def insertOutput(self, output):
		"""Inserts a output into the database.

		Does not commit database modification.
		@param output Output object.
		"""
		query = '	INSERT INTO outputs (transaction_id, value, address, script, index) \
					VALUES (%s, %s, %s, %s, %s)'
		self.executeQuery(query, (\
					self.lastId, \
					binaryRead.uLongLongToStr(output.value), \
					output.outputAddress, \
					binaryRead.strToHex(output.outputScript), \
					output.outputIndex))


#-------HELPER DATABASE FUNCTIONS

	def getLastOffset(self, fileName):
		"""Compute the last offset read of the last btc file parsed.

		@param fileName String containing the file name.
		@retval lastOffset[0] Value of the last offset.
		"""
		query = 'SELECT SUM(real_size) from blocks where file_name = %s'
		self.executeQuery(query, (fileName,))
		lastOffset = self.fetchOne()
		return lastOffset[0]

	def getBlockCount(self):
		"""Compute the count of blocks in the database.

		@retval rawBlock[0] The count of blocks in the database.
		"""
		query = 'SELECT * from blocks ORDER BY id DESC LIMIT 1'
		self.executeQuery(query)
		rawBlock = self.fetchOne()
		return rawBlock[0]

	def getTxCount(self):
		"""Compute the count of transactions in the database.

		@retval rawTransaction[0] The count of transactions in the database.
		"""
		query = 'SELECT * from transactions ORDER BY id DESC LIMIT 1'
		self.executeQuery(query)
		rawTransaction = self.fetchOne()
		return rawTransaction[0]

	def getInputCount(self):
		"""Compute the count of inputs in the database.

		@retval rawInput[0] The count of inputs in the database.
		"""
		query = 'SELECT * from inputs ORDER BY id DESC LIMIT 1'
		self.executeQuery(query)
		rawInput = self.fetchOne()
		return rawInput[0]

	def getOutputCount(self):
		"""Compute the count of outputs in the database.

		@retval rawOutput[0] The count of outputs in the database.
		"""
		query = 'SELECT * from outputs ORDER BY id DESC LIMIT 1'
		self.executeQuery(query)
		rawOutput = self.fetchOne()
		return rawOutput[0]

#-------CLUSTER FUNCTIONS

	def insertCluster(self):
		"""Inserts a cluster into the database.

		Does not commit database modification.
		"""
		query = '	INSERT INTO clusters (currency_amount) \
					VALUES (NULL) RETURNING id'
		self.executeQuery(query)
		self.setLastId()

	def insertAddress(self, address):
		"""Inserts an address into the database.

		Does not commit database modification.
		@param address Address object.
		"""
		query = '	INSERT INTO addresses (id, cluster_id) \
					VALUES (%s, %s)'
		self.executeQuery(query, (\
					address.Id, \
					address.clusterId))

	def aggregateAddresses(self, address1, address2):
		"""Regroups addresses related to a same cluster.

		@param address1 Address object.
		@param address2 Address object.
		"""
		query = 'SELECT * from addresses where id = %s or id = %s'
		self.executeQuery(query, (address1, address2))
		result = self.fetchAll()
		if result == None:
			self.insertCluster()
			self.insertAddress(Address.Address(address1, self.lastId))
			self.insertAddress(Address.Address(address2, self.lastId))
		elif len(result) > 1:
			return
		elif result[0] == address1:
			self.insertAddress(Address.Address(address2, self.lastId))
		else:
			self.insertAddress(Address.Address(address1, self.lastId))
		self.commit()

#-------LEDGER FUNCTIONS

	def getLedgerAtTime(self, address, timestamp):
		"""Retrieves all operations of a Bitcoin address until a specific time.

		@param address The address checked.
		@param timestamp The time specified in a timestamp format.
		"""
		query = 'SELECT * from ledger where address = %s and block_timestamp <= %s'
		self.executeQuery(query, (address, timestamp))
		rawLedgerLineList = self.fetchAll()
		ledgerBook = LedgerBook.LedgerBook()
		for rawLedgerLine in rawLedgerLineList:
			ledgerLine = Ledger.Ledger()
			ledgerLine.setLedgerLineFromDb(rawLedgerLine)
			ledgerBook.append(ledgerLine)
		return ledgerBook

	def isSeenAtTime(self, address, timestamp):
		"""Checks if a Bitcoin address has performed operations at a specific time.

		@param address The address checked.
		@param timestamp The time specified in a timestamp format.
		"""
		query = 'SELECT * from ledger where address = %s and block_timestamp < %s LIMIT 1'
		self.executeQuery(query, (address, timestamp))
		isSeen = self.fetchOne()
		if isSeen != None:
			return True
		else:
			return False

	def insertInputToLedger(self, input_):
		"""Inserts a ledger raw from an Input object.

		Does not inserts coinbases.
		@param input_ Intput object."""
		block = self.getBlockByTxId(input_.transactionId)
		output = self.getPreviousOutputFromInput(input_)
		if input_.isCoinbase == True or block.blockHeader.isOrphan == True or output == None:
			return
		query = '	INSERT INTO ledger (address, operation, value, block_timestamp) \
					VALUES (%s, %s, %s, %s)'
		self.executeQuery(query, (\
					output.outputAddress, \
					False, \
					output.value, \
					block.blockHeader.timestamp))
		self.commit()

	def insertOutputToLedger(self, output):
		"""Inserts a ledger raw from an Output object.

		@param output Output object.
		"""
		query = '	INSERT INTO ledger (address, operation, value, block_timestamp) \
					VALUES (%s, %s, %s, %s)'
		block = self.getBlockByTxId(output.transactionId)
		if block.blockHeader.isOrphan == True:
			return
		self.executeQuery(query, (\
					output.outputAddress, \
					True, \
					output.value, \
					block.blockHeader.timestamp))
		self.commit()


#-------MAIN CHAIN FUNCTIONS

	def getLastMainChainBlock(self):
		"""Retrieves last main chain block inserted into the database.

		@retval rawBlock List of raw datas of the last main chain block.
		"""
		query = 'SELECT * from blocks WHERE orphan = False ORDER BY id ASC LIMIT 1'
		self.executeQuery(query)
		rawBlock = self.fetchOne()
		if rawBlock is not None:
			block = Block.Block(None, rawBlock[0], rawBlock[9])
			block.setBlockFromDb(rawBlock)
			return block
		return rawBlock

	def getLastOrphanFlow(self, table):
		"""Retrieves last block of the database where orphan state is undefined.

		@param table Table name.
		@retval rawData List of raw datas of the block found.
		"""
		query = 'SELECT * from %s WHERE orphan = NULL ORDER BY id DESC LIMIT 1' % table
		self.executeQuery(query)
		rawData = self.fetchOne()
		if rawData is not None:
			return rawData[0]
		return rawData

	def getLastBlockByHeigth(self):
		"""Retrieves last main chain block inserted into the database.

		@retval rawBlock List of raw datas of the last main chain block.
		"""
		query = 'SELECT * from blocks WHERE real_number IS NOT NULL ORDER BY real_number DESC LIMIT 1'
		self.executeQuery(query)
		rawBlock = self.fetchOne()
		if rawBlock is not None:
			block = Block.Block(None, rawBlock[0], rawBlock[9])
			block.setBlockFromDb(rawBlock)
			return block
		return rawBlock

	def updateMainChain(self, prevBlockNumber, currentblockHash):
		"""Updates block orphan state and next_block_hash of the block.

		@param prevBlockNumber ID of the previous block.
		@param currentblockHash String containing block hash of the current block.
		"""
		query = 'UPDATE blocks SET next_block_hash = %s, orphan = False WHERE id = %s'
		self.executeQuery(query, (currentblockHash, prevBlockNumber))
		self.commit()

	def updateOrphanBlocks(self):
		"""Updates all block where orphan state is NULL to True."""
		query = 'UPDATE blocks SET orphan = True WHERE orphan = NULL'
		self.executeQuery(query)
		self.commit()

	def updateOrphanState(self, table, blockNumber, state):
		"""Updates a block orphan state.

		@param table The name of the table.
		@param blockNumber The block ID.
		@param state The orphan block state.

		"""
		query = 'UPDATE %s SET orphan = %s WHERE id = %s' % (table, state, blockNumber)
		self.executeQuery(query, (table, state, blockNumber))
		self.commit()

	def updateBlockHeigth(self, blockNumber, blockRealNumber):
		"""Updates a block heigth.

		@param blockNumber The block ID.
		@param blockRealNumber The block height.

		"""
		query = 'UPDATE blocks SET real_number = %s WHERE id = %s'
		self.executeQuery(query, (blockRealNumber, blockNumber))
		self.commit()

#-------TABLES GENERATION

	def createBlockTable(self):
		"""Creates Block table."""
		self.executeQuery(formatedQueries.blockTable)

	def createTransactionTable(self):
		"""Creates Transaction table."""
		self.executeQuery(formatedQueries.transactionTable)

	def createInputTable(self):
		"""Creates Input table."""
		self.executeQuery(formatedQueries.inputTable)

	def createOutputTable(self):
		"""Creates Output table."""
		self.executeQuery(formatedQueries.outputTable)

	def createClusterTable(self):
		"""Creates Cluster table."""
		self.executeQuery(formatedQueries.clusterTable)

	def createAddressTable(self):
		"""Creates Address table."""
		self.executeQuery(formatedQueries.addressTable)

	def createLedgerTable(self):
		"""Creates Ledger table."""
		self.executeQuery(formatedQueries.ledgerTable)

	def createDatabaseTables(self):
		"""Creates all database tables."""
		self.createBlockTable()
		self.createTransactionTable()
		self.createInputTable()
		self.createOutputTable()
		self.createClusterTable()
		self.createAddressTable()
		self.createLedgerTable()

	def createIndexes(self):
		"""Creates Indexes tables."""
		try:
			self.executeQuery(formatedQueries.transactionIndex)
			self.executeQuery(formatedQueries.outputIndex)
		except psycopg2.ProgrammingError:
			self.dbConnection.rollback()