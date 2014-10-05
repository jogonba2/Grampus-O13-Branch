#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile

def unzipXml(nameFile):
	with zipfile.ZipFile(nameFile,"r") as zipApk:
		return zipApk.open("AndroidManifest.xml","r")


def manageProcess(nameApk):   # main function
	# Parsing xml O(n)
	crudeText = ""
	i = 0
	xmlFile = unzipXml(nameApk)
	xmlRead = xmlFile.read()
	lenXml = len(xmlRead)
	while i != (lenXml):
		if xmlRead[i].isalnum() or xmlRead[i] == "." or xmlRead[i] == "/": # module to goodChar
			if ord(xmlRead[i+1]) == 0 and ord(xmlRead[i+2]) == 0: # x <space><space>	 
				crudeText += xmlRead[i] + "\n"
			else:
				crudeText += xmlRead[i]	
		i += 1
	xmlFile.close()
	return createDatadir(crudeText.rsplit("\n")) # str -> aux []

def createDatadir(crudeText):
	# Create data dir O(n)
	c = 0
	dataDir = {}
	for i in range (0,len(crudeText)):
		if len(crudeText[i]) > 2:
			dataDir["Field: " + str(c)] = crudeText[i]
			c += 1
	print dataDir
	return dataDir
		
# Total: O(2n)

if __name__ == "__main__":
	manageProcess("app.apk")

