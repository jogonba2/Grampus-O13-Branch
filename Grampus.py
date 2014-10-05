#!/usr/bin/python2
#-*- coding:utf-8 -*-
#Anyadir images y network
from PyQt4 import QtGui, QtCore
import Thread,os
import urllib,re

class GUI(QtGui.QWidget):

    def __init__(self):
		
		QtGui.QWidget.__init__(self)
		# Estructuras de datos auxiliares para trabajar con los datos obtenidos en masa
		self.fileOpenUrl = {}
		self.abiertos = []  
		self.__setAllConfig()
		self.__estilo()
		self.setLayout(self.mainLayout)
		self.__setConnections()
	
    def _setStatusBar(self,statusBar):
     	self.statusBar = statusBar
     	self.statusBar.showMessage(self.tr("Ready..."))
		
    def __cancelar(self):
		self.the().terminate()
	
    def __setConnections(self):
		#Conexiones
		self.connect(self.btnUrlCrawl,QtCore.SIGNAL('clicked()'),self.__configCrawler)
		self.connect(self.btnUrlFinger,QtCore.SIGNAL('clicked()'),self.__configFinger)
		self.connect(self.btnAbrir, QtCore.SIGNAL("clicked()"), self.__openFile)
		self.connect(self.lstAbiertos,QtCore.SIGNAL("itemClicked(QListWidgetItem *"), self.__chg)
		self.connect(self.tab,QtCore.SIGNAL('tabCloseRequested(int)'), self.__cerrar)
		self.connect(self.tab,QtCore.SIGNAL('currentChanged(int)'), self.__chgl)
		self.connect(self.lstAbiertos,QtCore.SIGNAL('currentRowChanged(int)'), self.__chg)
		self.connect(self.btnLimpiar,QtCore.SIGNAL('clicked()'), self.__closeAllElements)
		self.connect(self.btnCdata,QtCore.SIGNAL('clicked()'),self.__clearMetaData)
		self.connect(self.mergeButton,QtCore.SIGNAL('clicked()'),self.__mergeTabs)
		self.connect(self.downloadButton,QtCore.SIGNAL('clicked()'),self.__downloadAll)
		self.connect(self.downloadSelected,QtCore.SIGNAL('clicked()'),self.__downloadID)
		self.connect(self.cleanAllButton,QtCore.SIGNAL('clicked()'),self.__cleanAllMetadata)
   
    def __cleanAllMetadata(self):
		try:
			self.__cancelar()
		except:
			pass
		for file2Clean in self.abiertos:
			extFile2Clean = file2Clean[file2Clean.rfind('.')+1:]
			if extFile2Clean in ["pdf","doc","ppt","exe","docx","pptx","xlxs","mp3","odf","sxw","odp","odg","gif"]:
				try:
					self.the = Thread.Thread(file2Clean[file2Clean.rfind('.')+1:], file2Clean, None, None,None,"Clear")
					self.the.start()
				except:
					continue 	
		self.__endsClear()
		
    def __downloadID(self):
		idUrl, ok = QtGui.QInputDialog.getInteger(self,"Download Selected","Id Url")
		directory = str(QtGui.QFileDialog.getExistingDirectory(self, 'Open Directory', '').toAscii())
		if ok:
			self.__extractUrlById(idUrl,directory)

    def __extractUrlById(self,idUrl,directory):
		allUrls = str(self.tab.widget(self.tab.currentIndex()).toPlainText()).split('\n')
		for url in allUrls:
			if str(idUrl) == str(re.match("^\d*",url).group(0)):
				listUrl = [url]
				self.statusBar.showMessage(self.tr("Download started..."))
				# Le enviamos al thread id por extension para descarga unica, el string con la url, el nombre del tab para crear la carpeta y la operacion
				self.the = Thread.Thread("Id",(listUrl[0][listUrl[0].rfind(':',0,5)+1:]).strip(),None,None,directory,"Download")
				self.connect(self.the, QtCore.SIGNAL("EndsDownload"), self.__DownloadFinish)
				self.the.start()
				
    def __downloadAll(self):
		
		if self.tab.count()>0:
			self.statusBar.showMessage(self.tr("All download started..."))
			self.the = Thread.Thread(None, self.fileOpenUrl, None, None,None,"Download")
			self.connect(self.the, QtCore.SIGNAL("EndsDownload"), self.__DownloadFinish)
			self.the.start()    
				
    def _returnTab2Save(self):
		return self.tab	

    def __setIcons(self,text):
		if self.ext in ["pdf","docx", "pptx", "xlsx", "mdbx" , 'odt', 'odf', 'sxw', 'odp', 'odg', 'doc','xls','ppt','jpg','jpeg','gif','mp3','wav','exe']:
			icons = 'recursos/%s.png' % text.split('.')[-1]
		else:
			icons = 'recursos/web.png'
		return icons
		
    def __DownloadFinish(self):
		self.statusBar.showMessage(self.tr("All downloaded!"))
			
    def __mergeTabs(self):

		# Guardamos un diccionario que contiene la intersección de los tabText con el mismo nombre
		dictOfDataTab = {}
		for i in range(0,self.tab.count()):
			try:
				dictOfDataTab[str(self.tab.tabText(i))] +=  "<br><hr size='2'/><br>" + str(self.tab.widget(i).toHtml())	
			except:
				dictOfDataTab[str(self.tab.tabText(i))] = str(self.tab.widget(i).toHtml())
					
		# Eliminamos los tabs y los abiertos
		self.tab.clear()
		self.lstAbiertos.clear()
			
		# Creamos nuevos tabs y listwidgets con los datos del dict anterior
		for newName in dictOfDataTab:
			newNameText = QtGui.QTextEdit()
			newNameText.insertHtml(dictOfDataTab[newName])
			newNameText.setReadOnly(True)
			self.tab.addTab(newNameText,newName)
			icon = QtGui.QListWidgetItem()
			icon.setIcon(QtGui.QIcon(self.__setIcons(newName)))
			icon.setText(newName)
			self.lstAbiertos.insertItem(self.lstAbiertos.count(), icon)
			
    def __configFinger(self):
		try:
			self.__cancelar()
		except:
			pass 
		# El parámetro typeCrawler contendrá el tipo de tool finger a ejecutar
		Url = str(self.txtUrl.text())
		typeFinger = self.comboFinger.currentText()
		self.the = Thread.Thread(None, Url, None, None,typeFinger,"Finger",self.tab.widget(1))
		self.connect(self.the, QtCore.SIGNAL("StartsCrawler"), self.__startCrawler)
		self.connect(self.the, QtCore.SIGNAL("RestCrawlersUrl"), self.__addToTab)
		self.connect(self.the, QtCore.SIGNAL("RestCrawlersData"), self.__addMeta2Tab)
		self.connect(self.the, QtCore.SIGNAL("EndsCrawler"), self.__endsCrawler)
		self.the.start()
	
    # Construye los layouts de la izquierda y el central con sus items correspondientes: Tab && ListWidget
    def __setDefaultConfig(self):
		self.leftLayout = QtGui.QVBoxLayout()
		self.rightLayout = QtGui.QVBoxLayout()
		self.footerRightLayout = QtGui.QHBoxLayout()
		self.MLLayout = QtGui.QHBoxLayout()
		self.tab = QtGui.QTabWidget()
		self.tab.setTabsClosable(True)
		self.lstAbiertos = QtGui.QListWidget()
		self.lstAbiertos.setMaximumWidth(210)
		self.lstAbiertos.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.lstAbiertos.customContextMenuRequested.connect(self.__showContextMenu)
		self.leftLayout.addWidget(QtGui.QLabel('<center><b>Open Files</b></center>'))
		self.leftLayout.addWidget(self.lstAbiertos)
		self.leftLayout.addWidget(self.btnAbrir)
		self.rightLayout.addWidget(QtGui.QLabel('<center><b>Actual Work</b></center>'))
		self.rightLayout.addWidget(self.tab)
		self.footerRightLayout.addWidget(self.btnCdata)
		self.footerRightLayout.addWidget(self.cleanAllButton)
		self.footerRightLayout.addWidget(self.downloadSelected)
		self.footerRightLayout.addWidget(self.downloadButton)
		self.footerRightLayout.addWidget(self.mergeButton)
		self.footerRightLayout.addWidget(self.btnLimpiar)
		self.rightLayout.addLayout(self.footerRightLayout)
		self.MLLayout.addLayout(self.leftLayout)
		self.MLLayout.addLayout(self.rightLayout)
		
    def __startCrawler(self):
		self.statusBar.showMessage(self.tr("Operation Starts: Please, continue with your work"))	

    def __endsCrawler(self,nameReport):
		self.statusBar.showMessage(self.tr("Operation Ends: Work with "+nameReport+" is finished"))	
		os.chdir("..")

    # Construye el layout final que será el main layout del widget
    def __setAllConfig(self):
		self.__setMainButtons()	
		self.__setDefaultConfig()
		self.__setUrlConfig()
		self.mainLayout = QtGui.QHBoxLayout()
		self.mainLayout.addLayout(self.MLLayout)
		self.mainLayout.addWidget(self.frame)

    def __setUrlConfig(self):
		# Layouts del widget central crawler y finger de momento
		self.layoutCrawler = QtGui.QVBoxLayout()
		self.otherLayout = QtGui.QVBoxLayout()
		self.otherLayout.addStretch(0)
		self.layoutCrawler.addStretch(0)
		self.centralWidget = QtGui.QHBoxLayout()
		# Capa Principal que contiene a todas las demás
		self.MLayoutURL = QtGui.QVBoxLayout()
		self.MLayoutURL.addStretch(0)
		# Capa de Botones
		self.buttonLayout = QtGui.QHBoxLayout()
		
		#self.MLayoutURL.addStretch(1)
		self.frame = QtGui.QFrame()
		self.__setUrlOptions()
		self.frame.setLayout(self.MLayoutURL)
		# Change to 1 for layout separation
		self.MLayoutURL.addLayout(self.centralWidget)
		self.MLayoutURL.addLayout(self.buttonLayout)
		self.frame.hide()
	
    def __setUrlOptions(self):
		
		# Functions 
		self.comboExt = QtGui.QComboBox()
		self.comboCrawl = QtGui.QComboBox()
		for ext in ["Default","pdf","doc","ppt","jpg","exe","docx","pptx","xlxs","mp3","wav","odf","sxw","odp","odg","gif"]:
			self.comboExt.addItem(ext)
		for ctype in ["Grampus Crawler (Report in html)","Grampus Crawler (Report in tab)","Google","crawlertest","APK","pluginAPK","pluginAPK.py","Bing"]:
			self.comboCrawl.addItem(ctype)
		
		# Inicio de adición a la capa principal
		self.bannerPublicidad = QtGui.QLabel("<center><img src='recursos/banner.png'/></center>")
		#self.bannerPublicidad.setPixmap(QtGui.QPixmap("recursos/banner.png"))
		self.MLayoutURL.addWidget(self.bannerPublicidad)
		self.MLayoutURL.addWidget(QtGui.QLabel("<center><b>Web</b></center>"))
		self.txtUrl = QtGui.QLineEdit("http://")
		self.MLayoutURL.addWidget(self.txtUrl)
		
		# Functions
		self.comboProfundidad = QtGui.QComboBox()
		for i in range(1,6):
			self.comboProfundidad.addItem(str(i))
		
		# Finger
		self.comboFinger = QtGui.QComboBox()
		for ftype in ["Server Banner","Shodan","Grampus Header","Find Subdomains","Port Scanner","Sniffer"]:
			self.comboFinger.addItem(ftype)
		
		self.labelExtensions = QtGui.QLabel("<b>Extensions</b>")
		self.layoutCrawler.addWidget(self.labelExtensions)
		self.layoutCrawler.addWidget(self.comboExt)
		self.layoutCrawler.addWidget(QtGui.QLabel("<b>Crawler</b>"))
		self.layoutCrawler.addWidget(self.comboCrawl)
		self.layoutCrawler.addWidget(QtGui.QLabel("<b>Deepth</b>"))
		self.layoutCrawler.addWidget(self.comboProfundidad)
		self.otherLayout.addWidget(QtGui.QLabel("<b>Fingerprinting</b>"))
		self.otherLayout.addWidget(self.comboFinger)
		self.centralWidget.addLayout(self.layoutCrawler)
		self.centralWidget.addLayout(self.otherLayout)
		
		# Botones
		self.btnUrlCrawl = QtGui.QPushButton("Crawl")
		self.btnUrlFinger = QtGui.QPushButton("Finger")
		self.btnUrlCrawl.setIcon(QtGui.QIcon('recursos/crawler.gif'))
		self.btnUrlFinger.setIcon(QtGui.QIcon('recursos/fingerprinting.gif'))
		self.btnUrlCancelar = QtGui.QPushButton("Stop")
		self.btnUrlCancelar.setIcon(QtGui.QIcon('recursos/stop.png'))
		self.buttonLayout.addWidget(self.btnUrlCrawl)
		self.buttonLayout.addWidget(self.btnUrlFinger)
		self.buttonLayout.addWidget(self.btnUrlCancelar)
	 	
    def __configCrawler(self):	
		try:
			self.__cancelar()
		except:
			pass
		ext = self.comboExt.currentText()
		if ext == "Default":
			ext = ""
		Url = str(self.txtUrl.text())
		Profundidad = self.comboProfundidad.currentText()
		typeCrawl = self.comboCrawl.currentText()
		self.the = Thread.Thread(str(ext), Url, None, Profundidad,typeCrawl,"Crawler")
		if typeCrawl == "Grampus Crawler 1":
			self.connect(self.the, QtCore.SIGNAL("StartsCrawler"), lambda: self.__startCrawler())
			self.connect(self.the, QtCore.SIGNAL("EndsCrawler"), self.__endsCrawler)
		else:
			self.connect(self.the, QtCore.SIGNAL("StartsCrawler"), lambda: self.__startCrawler())
			self.connect(self.the, QtCore.SIGNAL("RestCrawlersUrl"), self.__addToTab)
			self.connect(self.the, QtCore.SIGNAL("RestCrawlersData"), self.__addMeta2Tab)
			self.connect(self.the, QtCore.SIGNAL("EndsCrawler"), self.__endsCrawler)
		self.the.start()
			
	# This method is deprecated, move it to Thread.py	
    def __clearMetaData(self):	
		try:
			self.__cancelar()
		except:
			pass
		# Sacamos el nombre del actual seleccionado
		currentItemText = self.lstAbiertos.currentItem().text()
		file2Clear = ""
		# Comparamos con los nombres de la lista self.abiertos
		for i in self.abiertos:
			fullNameAbierto = i[i.rfind('/')+1:]
			if fullNameAbierto == currentItemText:
				file2Clear = i
		if file2Clear != "":
			self.the = Thread.Thread(file2Clear[file2Clear.rfind('.')+1:], file2Clear, None, None,None,"Clear")
			self.connect(self.the, QtCore.SIGNAL("EndsClear"), self.__endsClear)
			self.the.start()	
		
    def __endsClear(self):
		self.statusBar.showMessage(self.tr("Cleared: Finish Clear"))
			
    def __Url(self):
        if self.frame.isHidden():
            self.frame.show()
        else:
            self.frame.hide()

    def __showContextMenu(self, position):
        if self.lstAbiertos.__len__():
            titulo = QtGui.QAction(self.lstAbiertos.currentItem().text(), self)
            titulo.setDisabled(True)
            separador = QtGui.QAction("", self)
            separador.setSeparator(True)
            limpiar = QtGui.QAction("Limpiar Metadatos", self)
            cerrar = QtGui.QAction("Cerrar", self)
            cerrar.triggered.connect(lambda: self.__cerrar(self.lstAbiertos.currentRow()))
            limpiar.triggered.connect(lambda: self.__Limpiar(self.lstAbiertos.currentRow()))
            menu = QtGui.QMenu()
            menu.addAction(titulo)
            menu.addAction(separador)
            menu.addAction(cerrar)
            menu.addAction(limpiar)
            menu.exec_(self.sender().mapToGlobal(position))

    def __Limpiar(self, index):
        self.__clearMetaData()
		
    def __cerrar(self, index):
        if self.fileOpenUrl:
			try:
				del self.fileOpenUrl[str(self.tab.tabText(index))]
			except:
				pass
        self.tab.removeTab(index)
        self.lstAbiertos.takeItem(index)
        del self.abiertos[index]
        self.__estilo()
		
	# Anyadir mas dinamismo al hidden con una variable auxiliar con contenido del tab
    def __estilo(self):
        if self.tab.__len__():
            self.tab.setStyleSheet('background-image: none')
            self.btnLimpiar.setEnabled(True)
            self.btnCdata.setEnabled(True)
            self.downloadButton.setEnabled(True)
            self.cleanAllButton.setEnabled(True)
            self.downloadSelected.setEnabled(True)
            
        else:
            self.tab.setStyleSheet('background-image: url(recursos/logo.png); background-position: center; background-repeat: none;')
            self.btnLimpiar.setEnabled(False)
            self.btnCdata.setEnabled(False)
            self.downloadButton.setEnabled(False)
            self.mergeButton.setEnabled(False)
            self.cleanAllButton.setEnabled(False)
            self.downloadSelected.setEnabled(False)

    def __chg(self):
        self.tab.setCurrentIndex(self.lstAbiertos.currentRow())

    def __chgl(self, index):
        self.lstAbiertos.setCurrentRow(index)

    def __openFile(self):
        self.archivo = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', '').toAscii())
        self.statusBar.showMessage(self.tr("Opening file..."))
        if self.archivo[self.archivo.rfind('.')+1:] in ["pdf","docx", "pptx", "xlsx", 'odt', 'odf', 'sxw', 'odp', 'odg', 'doc','xls','ppt','jpg','gif','mp3','wav','exe']:
			self.__ExtractMetadata(self.archivo)
        self.statusBar.showMessage(self.tr("File is opened"))
    
    def __openDirectory(self):
		self.directory = str(QtGui.QFileDialog.getExistingDirectory(self, 'Open Directory', '').toAscii())
		self.statusBar.showMessage(self.tr("Opening all files in dir..."))
		for file2Extract in os.listdir(self.directory):
			if file2Extract[file2Extract.rfind('.')+1:] in ["pdf","docx", "pptx", "xlsx", 'odt', 'odf', 'sxw', 'odp', 'odg', 'doc','xls','ppt','jpg','gif','mp3','wav','exe']:			
				finalFile = (self.directory+"/"+file2Extract).replace("\\","/")
				self.__ExtractMetadata(finalFile)
		self.statusBar.showMessage(self.tr("All files in dir are opened"))

    def __addToTab(self, item, isUrl):
		if isUrl == False:
			self.ext = item.split(".")[-1]
		else:
			self.ext = item
		index = self.tab.__len__()
		self.__icons(os.path.basename(item))
		self.tab.addTab(QtGui.QTextEdit(), os.path.basename(item))
		self.tab.setCurrentIndex(index)
		self.tab.currentWidget().setReadOnly(True)
		if self.ext in ["pdf","docx", "pptx", "xlsx", 'odt', 'odf', 'sxw', 'odp', 'odg', 'doc','xls','ppt','jpg','gif','mp3','wav','exe']:
			self.tab.setTabIcon(index, QtGui.QIcon('recursos/' + self.ext + '.png'))
		else:
			self.tab.setTabIcon(index, QtGui.QIcon('recursos/web.png'))
		self.lstAbiertos.setCurrentRow(index)
		self.__estilo()
		self.abiertos.append(item)

    def __ExtractMetadata(self, item):
        self.__addToTab(item,False)
        # Abiertos contiene los elementos del ListWidget de la izquierda.
        # Extension,Archivo,Index,Profundidad,Tipo de Crawler, Operacion
        self.the = Thread.Thread(self.ext, item, self.abiertos.index(item),None,None,"Extract")
        self.connect(self.the, QtCore.SIGNAL("Extract"), self.__addMeta2Tab)
        self.the.start()

    def __addMeta2Tab(self,data,data2,index,isUrl):
        
		if isUrl==True:
			self.fileOpenUrl[os.path.basename(data2)] = data
		if len(data)<=1:
			self.__actualizar("Status File:","Cleaned",index)
		else:
			for i in data:
				if type(data[i]).__name__ == "dict":
					for k in data[i]:
						self.__actualizar(k, data[i][k], index)
				elif type(data[i]).__name__ == "list":
					self.__actualizar(i, '<br/>'.join(data[i]), index)
				else:
					self.__actualizar(i, data[i], index)
		
    def __icons(self, text):
        icon = QtGui.QListWidgetItem()
        icon.setIcon(QtGui.QIcon(self.__setIcons(text)))
        icon.setText(text)
        self.lstAbiertos.insertItem(self.lstAbiertos.count(), icon)

    def __closeAllElements(self):
        self.tab.clear()
        self.lstAbiertos.clear()
        self.__estilo()
        for i in self.abiertos:
            self.abiertos.remove(i)
        self.fileOpenUrl = {}

    def __actualizar(self, uno, dos, index):
        if dos is None or dos=="":
            return False
        if dos is None or dos=="":
            return False
        if index!=None:
			try:
				self.tab.widget(int(index)).append('<font color="green"><b>%s:</b></font> %s<br/><br/>' % (uno, urllib.unquote(dos)))
			except:
				self.tab.widget(int(index)).append('<font color="green"><b>%s:</b></font> %s<br/><br/>' % (uno, dos))			
        else:
			try:
				self.tab.widget(self.tab.count()-1).append('<font color="green"><b>%s:</b></font> %s<br/><br/>' % (uno, urllib.unquote(dos)))
			except:
				self.tab.widget(self.tab.count()-1).append('<font color="green"><b>%s:</b></font> %s<br/><br/>' % (uno,dos))
    
    def __setMainButtons(self):
		# Buttons Declaration
		self.cleanAllButton = QtGui.QPushButton("Clear All")
		self.downloadSelected = QtGui.QPushButton("Download Selected")
		self.downloadButton = QtGui.QPushButton("Download All")
		self.mergeButton = QtGui.QPushButton("Merge")
		self.btnAbrir = QtGui.QPushButton('Open...')
		self.btnLimpiar = QtGui.QPushButton('Refresh')
		self.btnCdata = QtGui.QPushButton('Clear Selected')
		self.btnEnviar = QtGui.QPushButton('Enviar')
	
		# Config Buttons
		self.cleanAllButton.setIcon(QtGui.QIcon('recursos/cleanall.png'))
		self.downloadSelected.setIcon(QtGui.QIcon('recursos/selected.gif'))
		self.downloadButton.setIcon(QtGui.QIcon('recursos/download.png'))
		self.mergeButton.setIcon(QtGui.QIcon('recursos/merge.png'))
		self.btnAbrir.setIcon(QtGui.QIcon('recursos/open.png'))
		self.btnCdata.setIcon(QtGui.QIcon('recursos/cleardata.png'))
		self.btnLimpiar.setIcon(QtGui.QIcon('recursos/clear.png'))
		
		# Config Menu btnAbrir		
		menu = QtGui.QMenu()
		archivo = QtGui.QAction("File", self)
		url = QtGui.QAction("Url", self)
		directorio = QtGui.QAction("Directory", self)
		archivo.triggered.connect(lambda: self.__openFile())
		url.triggered.connect(lambda: self.__Url())
		directorio.triggered.connect(lambda: self.__openDirectory())
		menu.addAction(archivo)
		menu.addAction(url)
		menu.addAction(directorio)
		self.btnAbrir.setMenu(menu)
