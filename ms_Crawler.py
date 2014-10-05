# -*- coding: iso-8859-15 -*-
import re,urllib2,os
from shodan import WebAPI
from shodan.wps import GoogleLocation
import socket
import urllib2
import json,re,base64

class ms_GrampusCrawler:
	
	def __init__(self,url,totalResults,isIndex):
		###################################	
		self.initialCount = 0
		self.isIndex = isIndex
		self.url = url
		# Add more regExp -> list
		self.regExp = "(.*?)<a(.*?)href(.*?)=(.*?)[\"\'](.+?)[\"\'](.*?)"
		self.urlsCrawled = []
		self.otherInfo = {"Robots":"","CMS":"","Listing":""}

		####################################	
		self.__initOpener()
		if isIndex==True:
			self.__searchRobots()
			self.__searchCMS()
		self.__searchListing()
		self.__openUrl2Crawl(self.url)
		self.returnUrls()
	
	def __initOpener(self):
		self.opener = urllib2.build_opener()
		self.opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0"),
								  ("Host",self.url),("Referer:",self.url)]
	def __searchRobots(self):
		
		urlRobots = self.url+"/robots.txt"
		try:
			robotsRead = self.opener.open(urlRobots).read()
			if "User-agent" in robotsRead:
				self.urlsCrawled.append(urlRobots)
			self.otherInfo["Robots"] = robotsRead
		except:
			self.otherInfo["Robots"] = "None"
			pass
		self.__resetConnection() # Reseteamos Conexion para seguir con el crawleo
	
	def __searchCMS(self):
		
		read = self.opener.open(self.url).read()
		if "joomla" in read:
			self.otherInfo["CMS"] = "Joomla"	
		elif "WordPress" in read:
			self.otherInfo["CMS"] = "Wordpress"		
		elif "drupal" in read:
			self.otherInfo["CMS"] = "Drupal"
		elif "Smf" in read:
			self.otherInfo["CMS"] = "SMF"
		elif "phpbb" in read:
			self.otherInfo["CMS"] = "PhpBB"
		elif "vbulletin" in read:
			self.otherInfo["CMS"] = "vBulletin"
		elif "ipb" in read:
			self.otherInfo["CMS"] = "Ip Board"
		else:
			self.otherInfo["CMS"] = "NoN Cms"
		self.__resetConnection() # Reseteamos Conexion para seguir con el crawleo
	
	def __searchListing(self):
		
		if self.url[len(self.url)-1]=="/":
			url2Listing = self.url+".listing"
		else:
			url2Listing = self.url+"/.listing"
		try:
			read = self.opener.open(url2Listing).read()
			if "drwx" in read:
				self.urlsCrawled.append(url2Listing)
				self.otherInfo["Listing"] = read
		except:
			pass
		self.__resetConnection()
		
	
	def __resetConnection(self):
		
		self.opener.close()
		self.__initOpener()
		
	def __openUrl2Crawl(self,url):
		
		try:
			self.url2Crawl =  self.opener.open(url)
			self.__matchRegExp()
		except:
			pass
		
	def __matchRegExp(self):
		
		for linea in self.url2Crawl.readlines():
			regExpMatch = re.match(self.regExp,linea.strip().lower())
			self.__execComprobation(regExpMatch)			
	
	# Add in this method conditions to add new urls
	def __execComprobation(self,regExpMatch):
		
		if regExpMatch!=None and "http://" not in regExpMatch.group(5) and "/" not in regExpMatch.group(5) and "javascript" not in regExpMatch.group(5) and regExpMatch.group(5) not in self.urlsCrawled:				
			self.urlsCrawled.append(self.url+"/"+regExpMatch.group(5))
			self.initialCount += 1
		elif regExpMatch!=None and "http://" not in regExpMatch.group(5) and "/" in regExpMatch.group(5) and "javascript" not in regExpMatch.group(5) and regExpMatch.group(5) not in self.urlsCrawled:
			self.urlsCrawled.append(self.url+regExpMatch.group(5))
			self.initialCount += 1
		elif regExpMatch!=None and self.url in regExpMatch.group(5) and regExpMatch.group(5) not in self.urlsCrawled:
			self.urlsCrawled.append(regExpMatch.group(5))	
			self.initialCount += 1
	
	def returnUrls(self):	

		try:
			htmlSource = """<!DOCTYPE html><html><title>| Grampus Crawler |</title><head>
						<link rel=\"stylesheet\" type=\"text/css\" href=\"CSS.css\">
						<style type=\"text/css\">body {background-color: #356AA0 }
						div#menu {text-align: center; background-color: #C3D9FF; float: left;
						text-decoration: none;color: #666;width: 200px;border: solid #F9F7ED;}
						div#menu a:hover {background:none;text-decoration: underline;color:#fff;
						text-decoration:none;} div#links {background-color: #C3D9FF;width: 650px;
						font:bold 12px \"Trebuchet MS\";color: black; height: auto;float: center;text-align: center;
						margin: 0 auto;color: #666;border-bottom: 40px;padding: 40px;border: solid #F9F7ED;}
						div#footer {background-color: #C3D9FF;width: 800px;font:bold 12px \"Trebuchet MS\";text-align: center;
						margin: 0 auto; margin-top: 40px; border: solid #F9F7ED; color: #666;}</style>
						<center><img src=\"http://www.image-share.com/upload/2052/46.png\"></center></head><body>
						<div id=\"menu\"><nav><a href=\"/1\">Links</a><br> <a href=\"/2\">Robots</a><br><a href=\"/3\">Listing</a><br>
						<a href=\"/4\">CMS</a><br></div><div id=\"links\">"""
	
			if len(self.urlsCrawled) != 0:
				dumpCrawl = open(self.url.replace(".","").replace("://","").replace("-","").replace("/","")+".html","w")
				#dumpCrawl.write("<!DOCTYPE html><html><head><meta charset=\"utf-8\"""/><title>Dump Crawl</title></head><body bgcolor=#000000><header><div align=\"center\"><img src=\"http://www.image-share.com/upload/2052/46.png\"/></div></header><div align=\"center\">This web is Index<section>")
				dumpCrawl.write(htmlSource)
				for url in self.urlsCrawled:
					dumpCrawl.write("<article><header><a href=\""+url+"\">"+url+"</a></header></article><br>\r\n")
				try:
					for infoName in self.otherInfo:
						dumpCrawl.write("<br><br><header><h3><b>----> "+infoName+" <----</b></h3></header><br>")
						dumpCrawl.write(self.otherInfo[infoName])
				except:
					pass
				dumpCrawl.write("</div><div id=\"footer\">Generated by Grampus</div></body></html>")			
				dumpCrawl.close()
			return self.urlsCrawled				
		except:
			pass 

class ms_CrawlerManager:
	
	def __init__(self,url2Crawl):
		
		self.yaIniciado = False
		self.isIndex = True # Evitar rebusqueda de robots.txt
		self.url2Crawl = url2Crawl
		newDir = self.url2Crawl.replace("http://","").replace(".","").replace("/","").replace("www","")
		os.mkdir(newDir)
		os.chdir(newDir)
		self.__configure()
		
	def __configure(self):
		
		self.manager = ms_GrampusCrawler(self.url2Crawl,1000,self.isIndex)
		self.isIndex = False
		self.crawledList = []
		self.__loopCrawler()

	def __loopCrawler(self):	
		
		for urlCrawled in self.manager.returnUrls():
			try:
				if urlCrawled not in self.crawledList:
					self.crawledList.append(urlCrawled)
			except:
				continue
		if self.yaIniciado == False:
			self.__resetManagement()
					
	def __resetManagement(self):
	
		self.yaIniciado = True
		try:
			for urlCrawled in self.crawledList:
				self.url2Crawl = urlCrawled
				self.__configure()
		except:
			pass

class ms_ShodanCrawler:
	
	def __init__(self,search,typeSearch):		
		self.search = search
		self.typeSearch = typeSearch
		self.searchList = {}
		self.allCount = 0
		self.__initKey()
		self.__switchSearch()
		
	def __initKey(self):
			self.api = WebAPI("CvXzhcMm3YemfeNnNKE7ed9xRSCKfAhY")
				
	def __switchSearch(self):
		if self.typeSearch=="search":
			self.__execSearch()
		elif self.typeSearch=="lookup":
			self.search = socket.gethostbyname(self.search)
			self.webHost = self.api.host(self.search)
			self.__execLookup()
		#elif self.typeSearch=="mac":
		#	self.__macLocation()
			
	
	def __execSearch(self):
		searched = self.api.search(self.search)
		for search in searched["matches"]:
			try:
				self.searchList["Result "+str(self.allCount)] = {"Ip":search["ip"],"Updated":search["updated"],
				"Country":search["country_name"],"Latitude":search["latitude"],"Longitude":search["longitude"],
				"Port":search["port"],"Data":search["data"],"Os":search["os"]}
				self.allCount += 1
			except:
				continue
	
	def __execLookup(self):
		try:
			self.searchList["Result "+str(self.allCount)] = {"Ip":self.webHost["ip"],"Country":self.webHost["country_name"],"City":self.webHost["city"],
			"Os":self.webHost["os"],"Banner":self.webHost["data"][0]["banner"],"Port":self.webHost["data"][0]["port"],
			"TimeStamp":self.webHost["data"][0]["timestamp"]}
		except:
			print "Fail Lookup"
	
	#def __macLocation(self):

		
	def _returnData(self):
		return self.searchList

class ms_GoogleCrawler:
	
	def __init__(self,url,ext="",typeSearch=None):
		
		self.url = url
		self.ext = ext
		self.typeSearch = typeSearch
		self.search = ""
		self.startCount = 0
		self.filesWithExt = {}
		self.allCount = 0
		self.__switchFunction()
	
	def __switchFunction(self):
		
		if self.typeSearch==None:
			if self.ext!="":
				self.search = "q=inurl:"+self.url.replace("http://","//")+"+and+ext:"+self.ext
			else:
				self.search = "q=site:"+self.url
		else:
			self.search = "q=intext:"+self.url
		self.__extractUrls()
		
	def __extractUrls(self):
		
			# Coste cuadratico en peor caso n->inf, intentar reducir.
			while(True):
				try:
					# Proxy: &userip=53.22.11.65 (EJ)
					self.url2Crawl = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&"+self.search+"&start="+str(self.startCount)+"&rsz=large"
					connect_url2Crawl = urllib2.urlopen(self.url2Crawl)
					urls_Ext = json.load(connect_url2Crawl)
					urls_Json = urls_Ext["responseData"]["results"]
					for url_Extracted in urls_Json:
						self.filesWithExt[self.allCount] = url_Extracted["url"]
						self.allCount += 1
					connect_url2Crawl.close()
					self.startCount += 8
				except:
					break;

	def _returnUrls(self):

		return self.filesWithExt

class ms_G2Crawler():

    def __init__(self, Url, Profundidad, ext=""):
        self.Url = Url
        self.Profundidad = Profundidad
        AGENT = "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
        REFERER = Url
        self.ext = ext
        self.limit = 0
        EXPRESION = ".*?<a href.?=.?[\"\'](.*?)[\"\'].*?>"
        
        self.Regular = re.compile(EXPRESION, re.I)
        self.Crawled = []
        self.Crawl = [Url]
        self.Encontrados = []
        self.containsAll = {}
        self.fullDictionary = {}
        self.count = 0
        self.Cantidad = 0
        
        self.Opener = urllib2.build_opener()
        self.Opener.addheaders = [("User-Agent", AGENT), ("Host", Url), ("Referer", REFERER)]
        self.Crawler(self.Profundidad)
    
    def _returnUrls(self):
		if self.ext=="":
			return self.containsAll
		else:
			try:
				auxDictionary = {}
				self.count = 0
				for urlCrawled in self.containsAll:
					if urlCrawled[urlCrawled.rfind('.'):] in self.ext:
						auxDictionary[self.count] = urlCrawled
						self.count += 1
			except:
				pass
			return auxDictionary
		
    
    def Limpiar(self, Link):
        Buff = None
        for i in Link:
            if i.split(".")[-1] in self.ext:
				if not i in self.Encontrados:
				    self.Encontrados.append(i)
				    self.Cantidad += 1
                    #print len(self.Encontrados), "Encontrados"
            else:
                if i.startswith('/'):
                    Buff = self.Url + i
                elif i.startswith(self.Url):
                    Buff = i
                else:
                    if not i.startswith("http://")or not i.startswith("#"):
                        Buff = self.Url + "/" + i
                if not Buff == None:
                    if not Buff in self.Crawled:
                        self.Crawl.append(Buff)

    def Crawler(self, Profundidad):
        #print len(self.Crawl), "A revisar"
        if Profundidad > 0:
            for i in self.Crawl:
				if self.limit >= 100:
					break;
				self.limit += 1
				self.Abrir(i)
				try:
					self.Crawler(Profundidad - 1)
				except:
					continue
		
    
    def Abrir(self, Url):
        if Url in self.Crawled:
		    self.Crawl.remove(Url)
		    return
        #print "Abriendo", Url
        try:
			self.containsAll[self.count] = Url
			self.count += 1
			Data = self.Opener.open(Url).read()
			Links = self.Regular.findall(Data)
			self.Crawled.append(Url)
			self.Crawl.remove(Url)
			self.Limpiar(Links)
        except:
			pass

class ms_Bing():
	
	def __init__(self,search,extension="",typeSearch=None):
		self.search = search
		self.ext = extension
		self.typeSearch = typeSearch
		self.skipValue = 0
		self.urlDictionary = {}
		self.__switchExtension()
		self.__executeAuthentication()
		self.__executeSearch()
	
	def __switchExtension(self):
		
		if self.typeSearch==None:
			if self.ext!="":
				self.search = "site:"+self.search+"%20filetype:"+self.ext
			else:
				self.search = "site:"+self.search
		else:
			self.search = self.search
		
	def __executeAuthentication(self):
		
		self.request = urllib2.Request("https://api.datamarket.azure.com/Bing/Search/v1/Composite?Sources=%27web%27&Query=%27"+str(self.search)+"%27&$skip="+str(self.skipValue)+"&$format=json")
		user = "youruser"
		passwd = "yourpasswd"
		authentication = base64.encodestring("%s:%s" % (user,passwd)).replace("\n","")
		self.request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")
		self.request.add_header("Authorization","Basic %s"%authentication)
		self.resultQuery = urllib2.urlopen(self.request)
		
	def __executeSearch(self):
		
		queryJson = json.load(self.resultQuery)
		# Append Dictionary
		j = 0
		countUrl = 0
		i = 0
		while j<3:
			while(i<=100):
				try:
					self.urlDictionary[countUrl] = str(queryJson["d"]["results"][0]["Web"][i]["Url"])
					countUrl += 1
				except:
					try:
						self.urlDictionary[countUrl] = str(queryJson["d"]["results"][0]["Web"][i]["DisplayUrl"])
						countUrl += 1
					except:
						pass
				i += 1
			
			self.skipValue += countUrl
			j += 1
			self.__executeAuthentication()
			
	def _returnUrls(self):
		return self.urlDictionary	
			
class GrampusHTTP:
	
	def __init__(self,key,header):
		
		self.key = key
		self.header = header
		self.__selectUrls()
		
	def __searchUrls(self):
		
		# Desactivar ms_Bing y ms_GoogleCrawler para más eficiencia, o reducir las urls de Bing
		allUrls = ms_Bing(self.key,"",1)._returnUrls()
		allUrls.update(ms_GoogleCrawler(self.key,"",1)._returnUrls())
		allUrls.update(ms_BingWithoutApi(self.key)._returnUrls())
		print allUrls
		endUrls = {}
		for key in allUrls:
			endUrls[allUrls[key]] = ""
		return endUrls
	
	def __getHeaders(self,url):
		
		self.socketClient = socket.socket()
		try:
			#(socket.gethostbyname(self.__replacedUrl(url))
			self.socketClient.connect((self.__replacedUrl(url),80))
			self.socketClient.send("HEAD / HTTP/1.0\r\n\r\n")
			data = self.socketClient.recv(1024)
			return data
		except:
			return None
	
	def __getOptions(self,url):
		
		self.socketClient = socket.socket()
		try:
			self.socketClient.connect((self.__replacedUrl(url),80))
			self.socketClient.send("OPTIONS / HTTP/1.0\r\n\r\n")
			data = self.socketClient.recv(1024)
			indexAllow = data.find("Allow")
			data = data[indexAllow:data.find("\r\n",indexAllow)]
			return data
		except:
			return ""
	
	def __replacedUrl(self,url):
		url = url.replace("http://","")
		url = url[:url.find('/')]
		return url
			
	def __selectUrls(self):
		
		self.allUrls = self.__searchUrls()
		self.selectedUrls = {}
		for key in self.allUrls:
			try:
				self.allUrls[key] = self.__getHeaders(key)
				self.allUrls[key] += self.__getOptions(key)
				if self.header in self.allUrls[key]:
					self.selectedUrls[key] = self.allUrls[key]
			except:
				continue
	
	def _returnSelected(self):
		return self.selectedUrls
	
	def _returnAll(self):
		return self.allUrls
		
class ms_BingWithoutApi:
	
	def __init__(self,search):
		self.search = search
		self.urlSearch = "http://www.bing.com/search?q="+self.search+"&first="
		self.dictUrls = {}
		self.__searchWebs()
	
	def __searchWebs(self):
		
		count = 0
		indexDict = 0
		while(count<=200):
			urlOpen = urllib2.urlopen(self.urlSearch+str(count))
			urlRead = urlOpen.read()
			for url in re.findall("<h3><a href=\"(.*?)\"",urlRead,re.I):
				if "r.msn" not in url:
					self.dictUrls[indexDict] = url
					indexDict += 1
			count += 10
			urlOpen.close()
	
	def _returnUrls(self):
		
		return self.dictUrls
