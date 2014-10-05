#!/usr/bin/env python
import sys
#import pyexiv2
#import gif
import os

class extract_EXIF:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		self.metaDictionary = {}
		self.__openFile()
		self._extract()
	
	# Open File To Extract Metadata
	def __openFile(self):
		
		try:
			self.metaData = pyexiv2.ImageMetadata(self.pathFile)
			self.__extractMetadata()
		except:
			self.metaDictionary["Error"] = "Isn't JPG File"
	
	# Extract Metadata From Image With EXIF Especification
	def __extractMetadata(self):
		
		try:
			self.metaData.read()
		except:
			self.metaDictionary["Error"] = "Isn't a valid JPG"
			
		for self.data in self.metaData.exif_keys:
			try:
				self.metaDictionary[(self.metaData.__getitem__(self.data).key.replace("Exif.",""))] = (self.metaData.__getitem__(self.data)).value
			except:
				pass
		
			
	#Show Extracted Metadata From Image
	def _extract(self):
		
		return self.metaDictionary
		
			
class clean_EXIF:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		self.__replaceMetaData()
		print pathFile
	
	def __replaceMetaData(self):
		
		metaData = pyexiv2.metadata.ImageMetadata(self.pathFile)
		metaData.read()
		countKey = 0
		while countKey<=len(metaData.exif_keys):
			for keys in metaData.exif_keys:
				try:
					metaData.__delitem__(keys)
				except:
					continue
			metaData.write()
			countKey += 1

# ANYADIR METODO INDETECTABLES 
class extract_GIF:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		try:
			self.gifFile = gif.GifInfo(self.pathFile)
			self.dirMetaData = {"Version":self.gifFile.version,"Width":self.gifFile.width,
								"Height":self.gifFile.height,"LoopCount":self.gifFile.loopCount,"PixelAspect":self.gifFile.pixelAspect,
								"PaletteSize":self.gifFile.paletteSize,"BgColor":self.gifFile.bgColor,
								"Comments":self.gifFile.comments,"Text":self.gifFile.otherText}
		except:
			self.dirMetaData = {"Error":"Isn't a valid GIF"}
					
	def _extract(self):
		
		return self.dirMetaData
		
class clean_GIF:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		self.gifFile = gif.GifInfo(self.pathFile)
		self.dirMetaData = {"Version":self.gifFile.version,"Width":self.gifFile.width,
							"Height":self.gifFile.height,"LoopCount":self.gifFile.loopCount,"PixelAspect":self.gifFile.pixelAspect,
							"PaletteSize":self.gifFile.paletteSize,"BgColor":self.gifFile.bgColor,
							"Comments":self.gifFile.comments,"Text":self.gifFile.otherText}
	
	def _extract(self):
		
		return self.dirMetaData
