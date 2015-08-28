"""@package bitcoin

This file contains class declaration of Output.
"""
import binaryRead
from helperfunc import converter

class Output:
	"""This class represents a Bitcoin output."""
	def __init__(self, outputIndex):
		"""Output constructor."""
		self.id = None
		self.outputIndex = outputIndex
		self.transactionId = None
		self.value = None
		self.varInt = None
		self.scriptLength = None
		self.scriptLengthBinary = None
		self.outputScript = None
		self.outputScriptDecoded = None
		self.outputAddress = None
		self.isOrphan = None

	def __str__(self):
		"""Object string representation."""
		string = ("Id: ", str(self.id),\
					"\nOutput Index: ", str(self.outputIndex),\
					"\nTransaction Id: ", str(self.transactionId),\
					"\nValue: ", str(self.value),\
					"\nOutput Address: ", self.outputAddress,\
					"\nScript Data: ", self.outputScriptDecoded)
		return ''.join(string)

	def setValue(self, datFile):
		"""Sets output value."""
		self.value = binaryRead.readULongLong(datFile)

	def setVarInt(self, datFile):
		"""Sets varint."""
		self.varInt = binaryRead.readVarInt(datFile)

	def setScriptLength(self, datFile):
		"""Sets script length."""
		lengthTupple = binaryRead.checkVariableLengthInteger(datFile, self.varInt)
		self.scriptLength = lengthTupple[0]
		self.scriptLengthBinary = lengthTupple[1]

	def setOutputScript(self, datFile):
		"""Sets output script."""
		self.outputScript = binaryRead.readByteNumber(datFile, self.scriptLength)

	def setOutputScriptDecoded(self):
		"""Decodes binary script to hexadecimal value."""
		self.outputScriptDecoded = binaryRead.strToHex(self.outputScript)

	def formatType1(self):
		"""Checks the script format."""
		if self.scriptLength == 67 and self.outputScriptDecoded[0:2] == "41" and self.outputScriptDecoded[-2:] == "ac":
			return converter.ECDSAToAddress(self.outputScriptDecoded[2:-2])
		return False

	def formatType2(self):
		"""Checks the script format."""
		if self.scriptLength == 66 and self.outputScriptDecoded[-2:] == "ac":
			return converter.ECDSAToAddress(self.outputScriptDecoded[0:-2])
		return False

	def formatType3(self):
		"""Checks the script format."""
		if self.scriptLength >= 25 and self.outputScriptDecoded[0:2] == "76" and self.outputScriptDecoded[2:4] == 'a9':
			return converter.keyHashToAddress(self.outputScriptDecoded[6:46])
		return False

	def formatType4(self):
		"""Checks the script format."""
		if self.scriptLength == 5:
			return "Invalid"
		return False

	def formatType5(self):
		"""Checks the script format."""
		i = 0
		while i < (self.scriptLength - 46):
			if self.outputScriptDecoded[i:i+2] == '76' and self.outputScriptDecoded[i+2:i+4] == "a9":
				i += 6
				return converter.keyHashToAddress(self.outputScriptDecoded[i:i+40])
			i += 1
		return "Invalid"

	def setAddressFromScript(self):
		"""Checks the script format and converts it to a Bitcoin address."""
		self.outputAddress = self.formatType1()
		if self.outputAddress == False:
			self.outputAddress = self.formatType2()
		if self.outputAddress == False:
			self.outputAddress = self.formatType3()
		if self.outputAddress == False:
			self.outputAddress = self.formatType4()
		if self.outputAddress == False:
			self.outputAddress = self.formatType5()

	def setOutput(self, datFile):
		"""Sets Output from .dat file."""
		self.setValue(datFile)
		self.setVarInt(datFile)
		self.setScriptLength(datFile)
		self.setOutputScript(datFile)
		self.setOutputScriptDecoded()
		self.setAddressFromScript()

	def setOutputFromDb(self, rawOutput):
		"""Sets Output from a database raw."""
		self.id = rawOutput[0]
		self.transactionId = rawOutput[1]
		self.value = rawOutput[2]
		self.outputAddress = rawOutput[3]
		self.outputScriptDecoded = rawOutput[4]
		self.outputIndex = rawOutput[5]
		self.isOrphan = rawOutput[6]

	def toString(self):
		"""Human readable print."""
		print "@@@@@@ OUTPUT @@@@@@"
		print "Index: " + str(self.outputIndex)
		print "Value: " + binaryRead.uLongLongToStr(self.value)
		print "Varint: " + ''.join(str(self.varInt).encode('hex'))
		print "Script Length: " + str(self.scriptLength)
		print "Script Data Decoded: " + self.outputScriptDecoded
		print "Output Address: " + self.outputAddress
		print "@@@@@@@@@@@@@@@@@@@@"