import struct
from datetime import datetime

#TODO: use file.tell()
offset = 0

def readByte(datFile):
	"""Reads one byte from .dat file."""
	byte = datFile.read(1)
	if not byte:
		return False
	global offset
	offset += 1
	return byte[0]

def readByteNumber(datFile, byteNumber):
	"""Reads several bytes from .dat file."""
	global offset
	offset += byteNumber
	return datFile.read(byteNumber)

def readUShort(datFile):
	"""Reads two bytes from .dat file."""
	global offset
	offset += 2
	return datFile.read(2)[::-1]

def readUInt(datFile):
	"""Reads four bytes from .dat file."""
	global offset
	offset += 4
	return datFile.read(4)[::-1]

def readULongLong(datFile):
	"""Reads eigth bytes from .dat file."""
	global offset
	offset += 8
	return datFile.read(8)[::-1]

def readHash(datFile):
	"""Reads thirty-two bytes from .dat file."""
	global offset
	offset += 32
	return datFile.read(32)[::-1]

def readVarInt(datFile):
	"""Checks EOF."""
	byte = readByte(datFile)
	if byte == False:
		return False
	return ord(byte)

def readMagicID(datFile, intermediate):
	global offset
	offset += 3
	intermediate = intermediate + datFile.read(3)
	return intermediate[::-1]

#TODO: move in helperfunc.converter

def strToHex(buffer):
	"""Converts value to hexadecimal string."""
	return ''.join(a.encode('hex') for a in buffer)

def uIntToStr(buffer):
	"""Converts int binary value to string."""
	return str(struct.unpack('>I', buffer)[0])

def uLongLongToStr(buffer):
	"""Converts long binary value to string."""
	return str(struct.unpack('>Q', buffer)[0])

def binaryToTime(buffer):
	"""Converts long binary value to date string."""
	prettyPrint =  datetime.fromtimestamp(struct.unpack('>L', buffer)[0])
	return prettyPrint.strftime('%d %B %Y %H:%M:%S')

def checkVariableLengthInteger(datFile, varInt):
	"""Checks and gets real value of varint."""
	if varInt < 0xfd:
		return (varInt, '')
	elif varInt == 0xfd:
		binaryForm = readUShort(datFile)
		return (struct.unpack('>H', binaryForm)[0], binaryForm)
	elif varInt == 0xfe:
		binaryForm = readUInt(datFile)
		return (struct.unpack('>I', binaryForm)[0], binaryForm)
	elif varInt == 0xff:
		binaryForm = readULongLong(datFile)
		return (struct.unpack('>Q', binaryForm)[0], binaryForm)
	else:
		print "VarInt Failed"
		exit()