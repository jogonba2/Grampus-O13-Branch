import sys,wave
from ID3 import *

class extract_WAV:
	
	def __init__(self,pathFile):
		self.pathFile = pathFile
		self.metaData = {"ChunkSize":"","SubChunkSize":"","AudioFormat":"","NChannels":"",
		"SampleRate":"","ByteRate":"","BlockAlign":"","BitsPerSample":"","SubChunk2Size":"",
		"Sample1":"","Sample2":"","Sample3":"","Sample4":"","Sample5":"","Sample6":"","Sample7":"",
		"CompressType":"","CompressName":"","SampWidth":""}
		self.__extractHex()
		self.__extractMetaData()
		
	
	# Copy HEX File in to hexParse.txt
	def __extractHex(self):
		self.inputStream = ""
		try:
			self.wav = open(self.pathFile,"r")
		except:
			self.metaData = {}
			self.metaData["Error"] = "An error has ocurred opening the file"
		self.count = 0
		for self.line in self.wav.readlines():
			for self.byte in self.line:
				if self.count < 72:
					self.inputStream += self.byte.encode("hex")
				self.count += 1
		
	# Parse To Big Endian
	def __toBigEndian(self,value,typeData):
		self.value = value
		self.data = ""
		if len(self.value) == 8:
			for self.i in (6,7,4,5,2,3,0,1):
				self.data += self.value[self.i]
			self.__toDecimalValue(self.data,typeData)
		else:
			for self.i in (2,3,0,1):
				self.data += self.value[self.i]
			self.__toDecimalValue(self.data,typeData)
		
	# Extract all MetaData
	def __extractMetaData(self):
		try:
			self.wave = wave.open(self.pathFile)
			self.metaData["CompressType"] = self.wave.getcomptype()
			self.metaData["CompressName"] = self.wave.getcompname()
			self.metaData["SampWidth"] = self.wave.getsampwidth()
			self.wave.close()
		except:
			self.metaData["CompressType"] = self.metaData["CompressName"] = self.metaData["SampWidth"] = "Information Not Available"
		self.__toBigEndian(self.inputStream[8:16],"ChunkSize")
		self.__toBigEndian(self.inputStream[32:40],"SubChunkSize")
		self.__toBigEndian(self.inputStream[48:56],"SampleRate")
		self.__toBigEndian(self.inputStream[56:64],"ByteRate")
		self.__toBigEndian(self.inputStream[40:44],"AudioFormat")
		self.__toBigEndian(self.inputStream[44:48],"NChannels")
		self.__toBigEndian(self.inputStream[64:68],"BlockAlign")
		self.__toBigEndian(self.inputStream[68:72],"BitsPerSample")
		if self.inputStream[72:80] == "64617461":
			self.__toBigEndian(self.inputStream[80:88],"SubChunk2Size")
			self.__toBigEndian(self.inputStream[88:96],"Sample1")
			self.__toBigEndian(self.inputStream[96:104],"Sample2")
			self.__toBigEndian(self.inputStream[104:112],"Sample3")
			self.__toBigEndian(self.inputStream[112:120],"Sample4")
			self.__toBigEndian(self.inputStream[120:128],"Sample5")
			self.__toBigEndian(self.inputStream[128:136],"Sample6")
			self.__toBigEndian(self.inputStream[136:144],"Sample7")
		else:
			for self.mData in self.metaData:
				if self.metaData[self.mData] == "":
					self.metaData[self.mData] = "Information Not Available"
			
	
	# Convert Hex Data To Decimal Value
	def __toDecimalValue(self,value,typeData):
		self.value = value
		self.metaData[typeData] = int(self.value,16)
	
	def _extract(self):
		
		return self.metaData

class clean_WAV:
	
	def __init__(self):
		print "PROX IMPLEMENT"
		
class extract_MP3:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		self.metaData = {}
	
	def _extract(self):
		try:
			self.id3info = ID3(self.pathFile)
			for self.elemento in self.id3info.keys():
				self.metaData[self.elemento.lower().capitalize()] = str(self.id3info[self.elemento])
		except:
			self.metaData["Error"] = "Isn't a valid mp3 file"
		return self.metaData

class clean_MP3:
	
		def __init__(self, pathFile):
			self.pathFile = pathFile
			self.__cleanMetadata()
			
		def __cleanMetadata(self):
			
				self.id3info = ID3(self.pathFile)
				try:
						id3info['TITLE'] = ""
						id3info['ALBUM'] = ""
						id3info['COMMENT'] = ""
						id3info['ARTIST'] = ""
						id3info['YEAR'] = ""
						id3info['GENRE'] = ""
				except:
						pass
