#!/usr/bin/python
#-*- coding:utf-8 -*-
# Forensic Grampus - Grampus Project - Grampus Team
"""
Documentation from pefile official website :
    http://code.google.com/p/pefile/wiki/UsageExamples
"""

import os,pefile,hashlib,datetime

class extract_EXE():

    def __init__(self):
        self.Meta_Info = {}

    def _ms_do(self, sFileName):
        self.sFileName = sFileName
        self.__getPropInfo()
        print "Name of the File : %s"% self.File_Name
        print "Size of the File : %s bytes"% self.sFileSize
        print "-----------------"
        self.__getMetaPeinfo()

    def __getMetaPeinfo(self):
        pe = pefile.PE(self.sFileName)
        try:
            for fileinfo in pe.FileInfo:
                try:
                    #Extracting metainfo
                    if fileinfo.Key == 'StringFileInfo':
                        for st_table in fileinfo.StringTable:
                            for entry in st_table.entries.items():
                                print "%s: %s"% (entry[0], entry[1])
                    #Extracting translation
                    if fileinfo.Key == 'VarFileInfo':
                        for var in fileinfo.Var:
                            print "%s: %s"% var.entry.items()[0]
                except:
                    print "ERROR, Can't read Pe info from the file"
        except:
            print "ERROR"

    def __getPropInfo(self):
        #Extracting properties info
        self.File_Name = os.path.basename(self.sFileName)
        self.sFileSize = os.path.getsize(self.sFileName)
        #Extract hashes (md5 and sha1) with hashlib
        sFile = open(self.sFileName, 'rb')
        self.md5 = hashlib.md5()
        self.sha1 = hashlib.sha1()

    def _extract(self):
        #print "------------------"
        #print "MD5 Hash of %s:\t"%(self.File_Name), self.md5.hexdigest()
        #print "SHA1 Hash of %s:\t"%(self.File_Name), self.sha1.hexdigest()
        return self.Meta_Info

class clean_EXE:
	
	def __init__(self):
		print "PROX IMPLEMENT"
