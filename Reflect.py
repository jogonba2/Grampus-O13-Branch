#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
class Reflect:
	
	# Types -> Extension,Crawler,Fingerprinting
	def __init__(self,nameOption,typeOption,fileCode,typeExtension=None):
		
		self.nameOption = nameOption
		self.typeOption = typeOption
		self.fileCode = fileCode
		self.typeExtension = typeExtension
		self.__parseFile()
		
	def __parseFile(self):
		
		fileOpened = open(self.fileCode,"r")
		sourceCode = fileOpened.read()
		classIndex = sourceCode.find("class")
		self.classSource = sourceCode[classIndex+6:sourceCode.find(":",classIndex)]
		if self.typeOption == "Crawler":
			typefileOpened = open("ms_Crawler.py","a")
			typefileReaded = open("ms_Crawler.py","r")
			if self.classSource not in typefileReaded.read():
				typefileOpened.write(sourceCode)
			self.__setCrawlerConfig()
		elif self.typeOption == "Finger":
			typefileOpened = open("ms_Finger.py","a")
			typefileOpened.write(sourceCode)
		else:
			if self.typeExtension == "Document":
				typefileOpened = open("ms_Documents.py","a")
				typefileOpened.write(sourceCode)
			elif self.typeExtension == "Image":
				typefileOpened = open("ms_Images.py","a")
				typefileOpened.write(sourceCode)
			elif self.typeExtension == "Audio":
				typefileOpened = open("ms_Audio.py","a")
				typefileOpened.write(sourceCode)
			elif self.typeExtension == "Video":
				typefileOpened = open("ms_Video.py","a")
				typefileOpened.write(sourceCode)
			elif self.typeExtension == "Other":
				typefileOpened = open("ms_Others.py","a")
				typefileOpened.write(sourceCode)
		typefileOpened.close()
				
	def __setCrawlerConfig(self):	
		openGrampus = open("Grampus.py","r")
		writeGrampus = open("Grampus2.py","w")
		
		# Add name to ComboBox
		sourceGrampus = openGrampus.read()
		backupSource = sourceGrampus
		indexPattern = sourceGrampus.find("\"Bing\"")
		sourceGrampus = sourceGrampus[:indexPattern]+"\""+self.nameOption+"\","+sourceGrampus[indexPattern:]
		if self.nameOption not in backupSource:
			writeGrampus.write(sourceGrampus)
		else:
			writeGrampus.write(backupSource)
		openGrampus.close()
		writeGrampus.close()
		os.remove("Grampus.py")
		os.rename("Grampus2.py","Grampus.py")
		
		# Add conditional in Thread.py
		openThread = open("Thread.py","r")
		writeThread = open("Thread2.py","w")
		threadOverride = False
		sourceThread = openThread.read()
		backupSource = sourceThread
		addSource = """
		\telif self.typeCrawler == \"""" + self.nameOption + "\":" +"""
			\tself.Emitir(3,None)
			\tcrawlerResults = ms_Crawler."""+self.classSource+"""(self.archivo,self.ext)._returnUrls()
			\tself.Emitir(4,None,self.archivo)
			\tself.Emitir(5,crawlerResults,self.archivo,True)
		"""
		if addSource in sourceThread:
			threadOverride = True
		endIndex = sourceThread.find("# END CRAWLER")-1
		sourceThread = sourceThread[:endIndex]+addSource+sourceThread[endIndex:]
		if threadOverride==False:
			writeThread.write(sourceThread)
		else:
			writeThread.write(backupSource)
		openThread.close()
		writeThread.close()
		os.remove("Thread.py")
		os.rename("Thread2.py","Thread.py")
		
	#def __setFingerConfig(self):
		
#if __name__ == "__main__":
	#Reflect("APK","Other","pluginAPK.py")
