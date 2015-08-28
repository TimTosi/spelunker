#!/usr/bin/python
"""@package spelunkertest
Checks the valid state of database content.

This module uses unittest package in order to assert parsed block
with those provided by blockchain.info API.
"""
import unittest
import os
import glob
import sys
import ConfigParser
import datetime
from random import randint
import helperfunc.converter as converter
import helperfunc.debug as debug
import blockparser.BlockParser as BlockParser
import postgreDb.DatabaseWrapper as DatabaseWrapper
import clusterizer.Clusterizer as Clusterizer
import testsuite.HttpBlock as HttpBlock
import testsuite.HttpTransaction as HttpTransaction

def initConfig():
	if os.path.isfile("./config.ini") != True:
		print "config.ini missing."
		return False
	config = ConfigParser.ConfigParser()
	config.read("./config.ini")
	settings = {}
	databaseName = config.get("Config", "databaseName")
	userName = config.get("Config", "userName")
	userPassword = config.get("Config", "userPassword")
	if not databaseName or not userName:
		print "Error: Database name or User Name is missing."
		exit()
	settings["dbCredentials"] = "dbname='%s' user='%s' password='%s'" % (databaseName, userName, userPassword)
	return settings

class BlockTestCase(unittest.TestCase):
	"""This class regroups test cases for Block object."""
	@classmethod
	def setUpClass(cls):
		"""Set up class method.

		Establishes database connection, retrieves some blocks
		of the database and corresponding blocks on blockchain.info.
		"""
		cls.settings = initConfig()
		cls.db = DatabaseWrapper.DatabaseWrapper(cls.settings["dbCredentials"])
		cls.db.setDatabaseEnv()
		cls.block = cls.db.getBlockByNumber(randint(0, cls.db.getBlockCount()))
		cls.httpBlock = HttpBlock.HttpBlock(cls.block.blockHeader.blockHash)

	@classmethod
	def tearDownClass(cls):
		"""Tear Down class method.

		Closes database connection.
		"""
		cls.db.close()

	def testBlockHash(self):
		"""Assert the blockHash attribute of BlockHeader."""
		self.assertEqual(self.httpBlock['hash'], self.block.blockHeader.blockHash)

	def testBlockMerkleRoot(self):
		"""Assert the merkleRoot attribute of BlockHeader."""
		self.assertEqual(self.httpBlock['mrkl_root'], self.block.blockHeader.merkleRoot)

	def testBlockPreviousBlockHash(self):
		"""Assert the previousBlockHash attribute of BlockHeader."""
		self.assertEqual(self.httpBlock['prev_block'], self.block.blockHeader.previousBlockHash)

	def testBlockVersion(self):
		"""Assert the version attribute of BlockHeader."""
		self.assertEqual(self.httpBlock['ver'], self.block.blockHeader.version)

	def testBlockHeight(self):
		"""Assert the realNumber attribute corresponding to the height of BlockHeader."""
		self.assertEqual(self.httpBlock['height'], self.block.blockHeader.realNumber)

	def testBlockIsOrphan(self):
		"""Assert the isOrphan attribute of BlockHeader."""
		if self.httpBlock['main_chain'] == True:
			self.assertFalse(self.block.blockHeader.isOrphan)
		else:
			self.assertTrue(self.block.blockHeader.isOrphan)

	def testBlockLength(self):
		"""Assert the length attribute corresponding to the binary size of BlockHeader."""
		self.assertEqual(self.httpBlock['size'], self.block.blockHeader.length)

	def testBlockNonce(self):
		"""Assert the nonce attribute of BlockHeader."""
		self.assertEqual(self.httpBlock['nonce'], self.block.blockHeader.nonce)

	def testBlockTimestamp(self):
		"""Assert the timestamp attribute of BlockHeader."""
		blockTimestamp = datetime.datetime.fromtimestamp(float(self.httpBlock['time'])).strftime('%Y-%m-%d %H:%M:%S')
		self.assertEqual(blockTimestamp, self.block.blockHeader.timestamp.strftime("%Y-%m-%d %H:%M:%S"))


class TransactionTestCase(unittest.TestCase):
	"""This class regroups test cases for Transaction object."""
	@classmethod
	def setUpClass(cls):
		"""Set up class method.

		Establishes database connection, retrieves some transactions
		of the database and corresponding transactions on blockchain.info.
		"""
		cls.settings = initConfig()
		cls.db = DatabaseWrapper.DatabaseWrapper(cls.settings["dbCredentials"])
		cls.db.setDatabaseEnv()
		cls.transaction = cls.db.getTxById(randint(0, cls.db.getTxCount()))
		cls.httpTransaction = HttpTransaction.HttpTransaction(cls.transaction.transactionHash)

	@classmethod
	def tearDownClass(cls):
		"""Tear Down class method.

		Closes database connection.
		"""
		cls.db.close()

	def testTransactionHash(self):
		"""Assert the transactionHash attribute of Transaction."""
		self.assertEqual(self.httpTransaction['hash'], self.transaction.transactionHash)

	def testTransactionVersion(self):
		"""Assert the version attribute of Transaction."""
		self.assertEqual(self.httpTransaction['ver'], self.transaction.transactionVersion)

	def testTransactionLockTime(self):
		"""Assert the lockTime attribute of Transaction."""
		self.assertEqual(self.httpTransaction['lock_time'], self.transaction.lockTime)

	def testTransactionInputCount(self):
		"""Assert the inputCount attribute of Transaction."""
		self.assertEqual(self.httpTransaction['vin_sz'], self.transaction.inputCount)

	def testTransactionOutputCount(self):
		"""Assert the outputCount attribute of Transaction."""
		self.assertEqual(self.httpTransaction['vout_sz'], self.transaction.outputCount)

if __name__ == '__main__':
	for i in range(0, 10):
		suite = unittest.TestLoader().loadTestsFromTestCase(BlockTestCase)
		suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TransactionTestCase))
		unittest.TextTestRunner(verbosity=2).run(suite)