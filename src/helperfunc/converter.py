"""@package helperfunc

This file contains several functions used to convert formats and bitcoin addresses.
"""

import hashlib
import binascii
from helperfunc import debug

def strToBase256(string):
	"""Converts a string to base 256 format."""
	result = 0
	for char in string:
		result = result * 256 + ord(char)
	return result

def strToBase58(nb):
	"""Converts a value to base 256 format."""
	base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	result = ''
	while nb > 0:
		result = base58[nb % 58] + result
		nb /= 58
	return result

def keyHashToAddress(key):
	"""Converts a key hash to a Bitcoin address."""
	key = b'\x00' + binascii.unhexlify(key)
	intermediate = key
	key = hashlib.new('sha256', key).digest()
	key = hashlib.new('sha256', key).digest()
	key = intermediate + key[0:4]
	key = '1' + strToBase58(strToBase256(key))
	return key

def ECDSAToAddress(key):
	"""Converts a ECDSA key to a Bitcoin address."""
	key = hashlib.sha256(binascii.unhexlify(key)).digest()
	key = hashlib.new('ripemd160', key).digest()
	key = b'\x00' + key
	intermediate = key
	key = hashlib.new('sha256', key).digest()
	key = hashlib.new('sha256', key).digest()
	key = intermediate + key[0:4]
	key = '1' + strToBase58(strToBase256(key))
	return key

def inputToBinary(input_):
	"""Converts an Input object to its binary representation."""
	binaryInput = 	input_.transactionHash[::-1] + \
					input_.transactionIndex[::-1] + \
					chr(input_.varInt) + \
					input_.scriptLengthBinary[::-1] + \
					input_.scriptData + \
					input_.sequenceNumber[::-1]
	return binaryInput

def outputToBinary(output):
	"""Converts an Output object to its binary representation."""
	binaryOutput = 	output.value[::-1] + \
					chr(output.varInt) + \
					output.scriptLengthBinary[::-1] + \
					output.outputScript
	return binaryOutput

def blockHeaderToBlockHash(version, previousBlockHash, merkleRoot, timestamp, targetDifficulty, nonce):
	"""Converts a BlockHeader object to its hash representation."""
	blockHash = version[::-1] + \
				previousBlockHash[::-1] + \
				merkleRoot[::-1] + \
				timestamp[::-1] + \
				targetDifficulty[::-1] + \
				nonce[::-1]
	blockHash = hashlib.new('sha256', blockHash).digest()
	blockHash = hashlib.new('sha256', blockHash).digest()
	blockHash = binascii.hexlify(blockHash[::-1])
	return blockHash

def transactionToTransactionHash(version, inputVarInt, inputCount, inputList, outputVarInt, outputCount, outputList, lockTime):
	"""Converts a Transaction object to its hash representation."""
	transactionHash =	version[::-1] + chr(inputVarInt) + inputCount
	for input_ in inputList:
		transactionHash += inputToBinary(input_)
	transactionHash +=	chr(outputVarInt) + outputCount
	for output in outputList:
		transactionHash += outputToBinary(output)
	transactionHash += lockTime[::-1]
	transactionHash = hashlib.new('sha256', transactionHash).digest()
	transactionHash = hashlib.new('sha256', transactionHash).digest()
	transactionHash = binascii.hexlify(transactionHash[::-1])
	return transactionHash