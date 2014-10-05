from PyQt4 import QtGui, QtCore
import ms_Audio,ms_Documents,ms_Video,sys,os,time,Thread,ms_Crawler,ms_Images,ms_Finger
#import crawler,directoio
import urllib,os
class Thread(QtCore.QThread):

	# Operation -> Clean/Extract/Crawler
	# ext -> pdf,doc...
	# index 
    def __init__(self,ext,archivo=None,index=None,profundidad=None,typeCrawler=None,operation=None,auxData=None):
        QtCore.QThread.__init__(self)
        try:
			self.ext = ext.lower()
	except:
		    self.ext = False
        self.archivo = archivo
        self.index = index
        self.profundidad = profundidad
        self.typeCrawler = typeCrawler
        self.operation = operation
        self.auxData = auxData

    def __del__(self):
        self.wait()

    def run(self):
		
		# *** DOWNLOAD *** #
		if self.operation == "Download":
			if self.ext == "id":
				nameFolder = self.typeCrawler
				os.chdir(nameFolder)
				urllib.urlretrieve(self.archivo,self.archivo[self.archivo.rfind('/')+1:])
				os.chdir('..')		

			else:
				for nameUrl in self.archivo:
					if os.path.isdir(nameUrl)==False:			
						os.mkdir(nameUrl)
						os.chdir(nameUrl)
					else:
						os.chdir(nameUrl)
					for indexUrl in self.archivo[nameUrl]:
						downloadUrl = self.archivo[nameUrl][indexUrl]
						urllib.urlretrieve(downloadUrl,downloadUrl[downloadUrl.rfind('/')+1:])
				os.chdir("..")
			self.Emitir(7,None)
			
			
				
		# *** FINGER TOOLS *** #
		
		if self.operation == "Finger":
			if self.typeCrawler == "Server Banner":
				self.Emitir(3,None)
				self.Emitir(5,ms_Finger.serverBanner(self.archivo)._returnDictionary(),self.archivo,False)
				self.Emitir(4,None,self.archivo)
				#2Search Subdomains
				"""self.Emitir(3,None)
				ms_Finger.ms_Subdomains("twitter.com",self.auxData)"""
			elif self.typeCrawler == "Shodan":
				self.Emitir(3,None)
				crawlResults = ms_Crawler.ms_ShodanCrawler(self.archivo,"search")._returnData()
				self.Emitir(5,crawlResults,self.archivo,False)
				self.Emitir(4,None,self.archivo)
				
			elif self.typeCrawler == "Grampus Header":
				self.Emitir(3,None)
				# El formato sera Topic -h header
				findParam = self.archivo.find("-h")
				topic = self.archivo[0:findParam-1]
				header = self.archivo[findParam+2:]
				grampusHTTP = ms_Crawler.GrampusHTTP(topic,header)
				crawlResults = grampusHTTP._returnAll()
				self.Emitir(5,crawlResults,header+" in "+topic,False)
				# Add this to show good searches
				#crawlResults = grampusHTTP._returnSelected()
				#self.Emitir(5,crawlResults,header+" in "+topic,False)
				self.Emitir(4,None,header+" in "+topic)
		
				
		# *** CRAWLER *** #
		
		elif self.operation == "Crawler":
			if self.typeCrawler == "Grampus Crawler (Report in html)":
				self.Emitir(3,None)
				ms_Crawler.ms_CrawlerManager(self.archivo)
				self.Emitir(4,None,self.archivo)
				return 
			elif self.typeCrawler == "Google":
				self.Emitir(3,None)
				if self.ext == "default":
					crawlResults = ms_Crawler.ms_GoogleCrawler(self.archivo,"")._returnUrls()
					self.Emitir(5,crawlResults,self.archivo,True)
				else:
					crawlResults = ms_Crawler.ms_GoogleCrawler(self.archivo,self.ext)._returnUrls()
					self.Emitir(5,crawlResults,self.archivo,True)
				self.Emitir(4,None,self.archivo)
				return
			elif self.typeCrawler == "Grampus Crawler (Report in tab)":
				self.Emitir(3,None)
				crawlerResults = ms_Crawler.ms_G2Crawler(self.archivo,self.profundidad,self.ext)._returnUrls()
				self.Emitir(4,None,self.archivo)
				self.Emitir(5,crawlerResults,self.archivo,True)
				return
			elif self.typeCrawler == "Bing":
				self.Emitir(3,None)
				crawlerResults = ms_Crawler.ms_Bing(self.archivo,self.ext)._returnUrls()
				self.Emitir(4,None,self.archivo)
				self.Emitir(5,crawlerResults,self.archivo,True)
				
		
			elif self.typeCrawler == "crawlertest":
				self.Emitir(3,None)
				crawlerResults = ms_Crawler.crawlertest(self.archivo,self.ext)._returnUrls()
				self.Emitir(4,None,self.archivo)
				self.Emitir(5,crawlerResults,self.archivo,True)

		
			elif self.typeCrawler == "crawlertest":
				self.Emitir(3,None)
				crawlerResults = ms_Crawler.crawlertest(self.archivo,self.ext)._returnUrls()
				self.Emitir(4,None,self.archivo)
				self.Emitir(5,crawlerResults,self.archivo,True)
		
			# END CRAWLER
				
				
		# *** EXTRACT *** #
		
		elif self.operation == "Extract":
			if self.ext == "pdf":
				data = ms_Documents.extract_PDF()._extract(self.archivo)
			elif self.ext in ("docx", "pptx", "xlsx", "mdbx"):
				data = ms_Documents.extract_Office2007().extract(self.archivo)
			elif self.ext in ('odt', 'odf', 'sxw', 'odp', 'odg'):
				data = ms_Documents.extract_OpenOffice()._ms_do(self.archivo)
			elif self.ext in ('doc','xls','ppt'):
				data = ms_Documents.extract_Office2003(self.archivo)._extract()
			elif self.ext in ('jpg','jpeg','gif'):
				if self.ext in ('jpg','jpeg'):
					data = ms_Images.extract_EXIF(self.archivo)._extract()
				else:
					data = ms_Images.extract_GIF(self.archivo)._extract()
			elif self.ext in ('mp3','wav'):
				if self.ext=='mp3':
					data = ms_Audio.extract_MP3(self.archivo)._extract()
				else:
					data = ms_Audio.extract_WAV(self.archivo)._extract()
			elif self.ext=='exe':
				data = ms_Others.extract_EXE()._ms_do(self.archivo)._extract()
			self.Emitir(1, data, self.archivo)	
		
		# *** CLEAR *** #	
		elif self.operation == "Clear":
			if self.ext == "pdf":
				ms_Documents.clean_PDF(self.archivo)
			elif self.ext in ("docx", "pptx", "xlsx", "mdbx"):
				data = ms_Documents.extract_Office2007().extract(self.archivo)
			elif self.ext in ('odt', 'odf', 'sxw', 'odp', 'odg'):
				data = ms_Documents.extract_OpenOffice()._ms_do(self.archivo)
			elif self.ext in ('doc','xls','ppt'):
				data = ms_Documents.clean_Office2003(self.archivo)
			elif self.ext in ('jpg','jpeg','gif'):
				if self.ext in ('jpg','jpeg'):
					data = ms_Images.clean_EXIF(self.archivo)
				#else:
				#	data = ms_Images.extract_GIF(self.archivo)._extract()
			elif self.ext in ('mp3','wav'):
				if self.ext=='mp3':
					data = ms_Audio.clean_MP3(self.archivo)
				#else:
				#	data = ms_Audio.extract_WAV(self.archivo)._extract()
			#elif self.ext=='exe':
			#	data = ms_Others.extract_EXE()._ms_do(self.archivo)._extract()
			self.Emitir(6,None,None)
	# Data -> info extraida Data2 -> Nombre de archivo
    def Emitir(self, Opt, data, data2=None, isUrl=False):
        time.sleep(0.3)
        if Opt == 1:
			self.emit(QtCore.SIGNAL("Extract"),data,data2,self.index,False)
        elif Opt == 3:
			self.emit(QtCore.SIGNAL("StartsCrawler"))
	elif Opt == 4:
		print data2
		self.emit(QtCore.SIGNAL("EndsCrawler"), data2)
	elif Opt == 5:
		self.emit(QtCore.SIGNAL("RestCrawlersUrl"),data2,True)
		# Se emite tambien data2 que contiene el nombre para agregar a la lista de urls.
		self.emit(QtCore.SIGNAL("RestCrawlersData"),data,data2,self.index,isUrl)
	elif Opt == 6:
		self.emit(QtCore.SIGNAL("EndsClear"))
	elif Opt == 7:
		self.emit(QtCore.SIGNAL("EndsDownload"))
		
