#!/usr/bin/env python
# -*- coding: utf-8 -*-

###### POC OF PLUGIN MANAGER ######
import urllib2,urllib,Reflect,json,os

class pluginGestor():
	
	def __init__(self):		
		self.__loopGestor()
	
	def __loopGestor(self):
		while True:
			if os.name=="nt":
				os.system("cls")
			else:
				os.system("clear")
			print """  
  ________                                          
 /  _____/___________    _____ ______  __ __  ______
/   \  __\_  __ \__  \  /     \\____ \|  |  \/  ___/
\    \_\  \  | \// __ \|  Y Y  \  |_> >  |  /\___ \ 
 \______  /__|  (____  /__|_|  /   __/|____//____  >
        \/           \/      \/|__|              \/ 
"""
			print "\n1:Show All Plugins\n2:Search Plugin\n3:Install Plugin\n4:Download\n5:Setup\n"
			numAction = input("Action> ")
			if self.__isNumber(numAction):
				if numAction==1:
					self.__showPlugins()
				elif numAction==2:
					namePlugin = raw_input("Search> ")
					self.__searchPlugins(namePlugin)
				elif numAction==3:
					namePlugin = raw_input("Plugin Name> ")
					typePlugin = raw_input("Type Plugin> ")
					filePlugin = raw_input("File Plugin> ")
					Reflect.Reflect(namePlugin,typePlugin,filePlugin)
				elif numAction==4:
					idDownload = raw_input("Id> ")
					self.__downloadPlugin(idDownload)
				elif numAction==5:
					self.__setupGrampus()
				raw_input()
				
	def __showPlugins(self):
		openUrl = urllib.urlopen("http://localhost/download.php?id=0&function=show")
		print openUrl.read().replace("<br>","\n")
	
	def __searchPlugins(self,namePlugin):
		openUrl = urllib.urlopen("http://localhost/download.php?name="+namePlugin+"&function=search")
		print openUrl.read().replace("<br>","\n")
		
	def __downloadPlugin(self,idDownload):
		openUrl2 = urllib.urlopen("http://localhost/download.php?id="+str(idDownload)+"&function=return")
		link = openUrl2.read()
		try:
			urllib.urlretrieve(link,link[link.rfind('/')+1:])
			print "[+] Plugin Downloaded with name: "+link[link.rfind('/')+1:]+" !\n\n"
		except:
			print "[-] Problems Downloading "
	
	def __setupGrampus(self):
		os.system("python setup.py install")

	def __isNumber(self,number):
		try:
			float(number)
			return True
		except:
			return False
		
pluginGestor()
		
		
