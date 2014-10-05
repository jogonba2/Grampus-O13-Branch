from flvlib import tags

class ms_FLV:
	
	def __init__(self,pathFile):
		self.pathFile = pathFile
		self.dirMetaData = {"Offset":"","Size":"","TimeStamp":"","SoundFormat":"",
							"SoundRate":"","SoundSize":"","SoundType":"","AACPacketType":"",
							"FrameType":"","CodecId":"","H264PacketType":""}
		self.__extractMetaData()
	def __extractMetaData(self):
		
		self.filex = open(self.pathFile)
		self.flv = tags.FLV(self.filex)
		self.flv = self.flv.parse_header
		self.tags = tags.Tag(self.flv,self.filex)
		self.tags.parse_tag_content()

class clean_FLV:
	
	def __init__(self):
		print "PROX IMPLEMENT"
