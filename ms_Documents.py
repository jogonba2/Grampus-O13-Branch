#!/usr/bin/python
#-*- coding:utf-8 -*-
import OleFileIO_PL
from xml.dom.minidom import parse
from tempfile import mkdtemp
from shutil import rmtree, copyfileobj
from zipfile import ZipFile, is_zipfile
import os,re,sys
from pyPdf import PdfFileReader,PdfFileWriter
from pyPdf.generic import createStringObject

class extract_Office2007():
    def __init__(self):
        self.fecha = {"01": "Enero",
        "02": "Febrero",
        "03": "Marzo",
        "04": "Abril",
        "05": "Mayo",
        "06": "Junio",
        "07": "Julio",
        "08": "Agosto",
        "09": "Septiembre",
        "10": "Octubre",
        "11": "Noviembre",
        "12": "Diciembre"}

        self.metaDatos = {"Titulo": "",
        "Usuarios": [],
        "Fecha": {"Creado": "", "Modificado": "", "Impreso": ""},
        "Aplicacion": "",
        "Empresa": "",
        "Editado": ""}

    def extract(self, archivo):
        self.archivo = archivo
        self.ruta = mkdtemp(prefix='gra')
        if self.__descomprimir():
            self.__docProps()
            self.__extraData()
        else:
            return {"Error": "No es un archivo valido"}
        rmtree(self.ruta)

        return self.metaDatos

    def __descomprimir(self):
        if not is_zipfile(self.archivo):
            return False
        buff = ZipFile(self.archivo, 'r')
        for i in buff.namelist():
            if i in ('docProps/core.xml', 'docProps/app.xml',
                'word/document.xml', 'word/_rels/document.xml.rels'):
                filename = os.path.basename(i)
                source = buff.open(i)
                target = file(os.path.join(self.ruta, filename), 'wb')
                copyfileobj(source, target)
                source.close()
                target.close()
        return True

    def __docProps(self):
        core = parse(os.path.join(self.ruta, 'core.xml'))
        app = parse(os.path.join(self.ruta, 'app.xml'))

        self.metaDatos["Usuarios"].append(
        self.__getMetaData(core, "dc:creator"))
        self.metaDatos["Titulo"] = \
        self.__getMetaData(core, "dc:title")
        self.metaDatos["Usuarios"].append(
        self.__getMetaData(core, "cp:lastModifiedBy"))

        self.metaDatos["Aplicacion"] = self.__getMetaData(app, "Application")
        self.metaDatos["Empresa"] = self.__getMetaData(app, "Company")
        self.metaDatos["Editado"] = \
        self.__getMetaData(core, "cp:revision") + " veces"

        self.metaDatos["Fecha"]["Creado"] = \
        self.__W3CDTF(self.__getMetaData(core, "dcterms:created"))
        self.metaDatos["Fecha"]["Modificado"] = \
        self.__W3CDTF(self.__getMetaData(core, "dcterms:modified"))
        self.metaDatos["Fecha"]["Impreso"] = \
        self.__W3CDTF(self.__getMetaData(core, "cp:lastPrinted"))

    def __W3CDTF(self, fecha):
        if fecha is None:
            return "Nunca"
        return str(fecha[5:7] + " de " + self.fecha[fecha[5:7]] + " del " +
        fecha[0:4] + " a las: " + fecha[14:19])

    def __getMetaData(self, xml, tag):
        buff = xml.getElementsByTagName(tag)
        if len(buff):
            if not buff[0].firstChild is None:
                return buff[0].firstChild.toxml()
            else:
                return None

    def __extraData(self):
        self.metaDatos["Links"] = []
        doc = os.path.join(self.ruta, 'document.xml')
        rel = os.path.join(self.ruta, 'document.xml.rels')
        if os.path.isfile(doc) and os.path.isfile(rel):
            document = parse(doc)
            links = parse(rel)

            buff = document.getElementsByTagName('w:ins')
            if len(buff):
                for i in buff:
                    usuario = i.getAttribute('w:author')
                    if not usuario in self.metaDatos["Usuarios"]:
                        self.metaDatos["Usuarios"].append(usuario)

            buff = links.getElementsByTagName('Relationship')
            if len(buff):
                for i in buff:
                    if i.getAttribute('TargetMode'):
                        link = i.getAttribute('Target')
                        if not link in self.metaDatos["Links"]:
                            self.metaDatos["Links"].append(link)
"""
class clean_Office2007:
	
	def __init__(self,fileName):
		self._ms_do(fileName, (fileName[0:fileName.rfind('.')]+"CLEANED"+fileName[fileName.rfind('.'):]))

	def _ms_do(self, sDocName, newDocName):
		self.sDocName = sDocName
		self.newDocName = newDocName
		self.ErrorDic = {}
		try:
			self.__uncompress()
		except:
			self.ErrorDic['Error'] = 'An error has ocurred uncompressing'
		try:
			self._xml_cleaner()
		except:
			self.ErrorDic['Error'] = 'An error has ocurred cleaning metadata'

		self.__compress()
		self._meta_adder()
		self._image_manag()
		try:
			os.remove(self.sDocName)
			os.rename(self.newDocName, self.sDocName)
		except:
			self.ErrorDic['Error'] = 'An error has ocurred writing the file'


	def __uncompress(self):
		#Uncompressing core.xml and app.xml to edit metadata
		if not zipfile.is_zipfile(self.sDocName):
			return False
		buff = zipfile.ZipFile(self.sDocName, 'r')
		for i in buff.namelist():
			if i in ('docProps/core.xml', 'docProps/app.xml'):
				filename = os.path.basename(i)
				source = buff.open(i)
				target = file(os.path.join(filename), 'wb')
				copyfileobj(source, target)
				source.close()
				target.close()
		return True

	def _xml_cleaner(self):
		#parsing core.xml to replace the values
		core = parse(os.path.join('core.xml'))
		corelist = ['dc:creator', 'dc:title', 'cp:lastModifiedBy', 'cp:revision',
					'dcterms:created', 'dcterms:modified', 'cp:lastPrinted']
		for i in corelist:
			try:
				core.getElementsByTagName(i)[0].childNodes[0].nodeValue = ""
			except:
				continue
		#saving
		f = open(os.path.join('core.xml'), 'w')
		core.writexml(f)
		f.close()
		#parsing app.xml to replace values
		app = parse(os.path.join('app.xml'))
		applist = ['Application', 'Company']

		for x in applist:
			try:
				app.getElementsByTagName(x)[0].childNodes[0].nodeValue = ""
			except:
				continue
        #saving
		j = open(os.path.join('app.xml'), 'w')
		app.writexml(j)
		j.close()

	def __compress(self):
        #creating the new doc
		zf = zipfile.ZipFile(self.sDocName, 'r')
		zp = zipfile.ZipFile(self.newDocName, 'w')
		try:
			for item in zf.infolist():
				buffer = zf.read(item.filename)
				#core and app .xml will be joined later in meta_adder func
				if (item.filename[-8:] != 'core.xml') and (item.filename[-7:] != 'app.xml') and (item.filename[-5:] != '.jpeg'):
					zp.writestr(item, buffer)
			zf.close()
			zp.close()
		except:
			self.ErrorDic['Error'] = "compressing error"

	def _meta_adder(self):
    #joining core and app.xml
		zf = zipfile.ZipFile(self.newDocName, 'a')
		try:
			zf.write('core.xml')
			zf.write('app.xml')
			zf.close()
		except:
			self.ErrorDic['Error'] = "error in writting"
        #removing core and app .xml because it's already joined
		os.remove('core.xml')
		os.remove('app.xml')


#adding another functions to clean exif metadata from the images where are into the 2007 office documents

	def __img_uncompress(self):
		buff = zipfile.ZipFile(self.sDocName, 'r')
		for name in buff.namelist():
			#we must to add another extensions
			if (name.find('.jpeg')!= -1):
				buff.extract(name)

	def _img_meta_extractor(self):
		ext = self.sDocName[self.sDocName.rfind('.'):]
		if ext == '.docx':
			images = os.listdir('word/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('word/media/%s'%(i), "word/media/image%s.jpg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue

			images = os.listdir('word/media/')
			var = 0
			while (var<5):
				for x in images:
					obj = Exif.clean_EXIF('word/media/%s'% x)
				var = var+1
		
		elif ext == '.pptx':
			images = os.listdir('ppt/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('ppt/media/%s'%(i), "ppt/media/image%s.jpg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue

			images = os.listdir('ppt/media/')
			var = 0
            while (var<5):
                for x in images:
                    obj = Exif.clean_EXIF('ppt/media/%s'% x)
                var = var+1

        elif ext == '.xlsx':
            images = os.listdir('xl/media/')
            counter = 0
            for i in images:
                counter = counter+1
                try:
                    os.rename('xl/media/%s'%(i), "xl/media/image%s.jpg"%(counter))
                except:
                    self.ErrorDic['Error'] = "an error has ocurred renaming the images"
                    continue

            images = os.listdir('xl/media/')
            var = 0
            while (var<5):
                for x in images:
                    obj = Exif.clean_EXIF('xl/media/%s'% x)
                var = var+1

	def _adder(self):
        #before to add the cleaned images into the document
        #we must to change the ext again
		var = self.sDocName[self.sDocName.rfind('.'):]
		if var == '.docx':
			images = os.listdir('word/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('word/media/%s'%(i), "word/media/image%s.jpeg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue

			zf = zipfile.ZipFile(self.newDocName, 'a')
			images = os.listdir('word/media/')
			for x in images:
				try:
					zf.write('word/media/%s'% x)
				except:
					self.ErrorDic['Error'] = "error in Writing"
					sys.exit(0)
			zf.close()
			rmtree('word/')

		if var == '.pptx':
			images = os.listdir('ppt/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('ppt/media/%s'%(i), "ppt/media/image%s.jpeg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue
			zf = zipfile.ZipFile(self.newDocName, 'a')
			images = os.listdir('ppt/media/')
			for x in images:
				try:
					zf.write('ppt/media/%s'% x)
				except:
					self.ErrorDic['Error'] = "error in Writing"
					sys.exit(0)
			zf.close()
			rmtree('ppt/')

		if var == '.xlsx':
			images = os.listdir('xl/media/')
			counter = 0
			for i in images:
				counter = counter+1
				try:
					os.rename('xl/media/%s'%(i), "xl/media/image%s.jpeg"%(counter))
				except:
					self.ErrorDic['Error'] = "an error has ocurred renaming the images"
					continue
			zf = zipfile.ZipFile(self.newDocName, 'a')
			images = os.listdir('xl/media/')
			for x in images:
				try:
					zf.write('xl/media/%s'% x)
				except:
					print "error in Writing"
					sys.exit(0)
			zf.close()
			rmtree('xl/')

	def _image_manag(self):
		self.__img_uncompress()
		self._img_meta_extractor()
		self._adder()
"""
class extract_Office2003:
	
	def __init__(self,docFile):
		
		self.docFile = docFile
		self.metaData = {}
		self.__initOleFile()
		self.__detectType()
	
	def __initOleFile(self):
		
		if OleFileIO_PL.isOleFile(self.docFile)==False:
			self.metaData["Error"] = "Isn't an Ole File"
		else:
			self.oleFile = OleFileIO_PL.OleFileIO(self.docFile)
	
	# Actually only support Word,Excel,PowerPoint. It's easy add more extensions :D
	""" Extensions are separated by groups because Excel and Word need
		SummaryInformation but ppt no and it doesn't add extra information, there are also other areas such as
		Current User or Pictures.
	"""
	def __detectType(self):
		
		for docType in [['Workbook'],['WordDocument'],['PowerPoint Document']]:
			if docType in self.oleFile.listdir():
				self.__manageExtraction(docType)
	
	def __manageExtraction(self,docType):
		
		if docType==['WordDocument'] or docType==['Workbook']:
			self.__extractDocument()
		else:
			self.__extractPresentation()
	
	def __extractDocument(self):
		
		for oleDir in self.oleFile.listdir():
			try:
				Properties = self.oleFile.getproperties(oleDir)
				for propertie in Properties:
					try:
						self.__oleFileIndex(propertie,Properties)
					except:
						continue
			except:
				continue
		# Add size to metadata table because it isn't returned in getproperties method
		try:
			self.metaData["Size"] = self.oleFile.get_size("WordDocument")
		except:
			self.metaData["Size"] = self.oleFile.get_size("Workbook")
	
	def __oleFileIndex(self,propertie,Properties):
		
		if propertie==8:
			self.metaData["Last Author"] = str(Properties[propertie])
		elif propertie==3:
			self.metaData["Assumpt"] = str(Properties[propertie])
		elif propertie==18:
			self.metaData["Tool"] = str(Properties[propertie])
		elif propertie==4:
			self.metaData["Author"] = str(Properties[propertie])
		elif propertie==9:
			self.metaData["Revisions"] = str(Properties[propertie])
		elif propertie==2:
			self.metaData["Title"] = str(Properties[propertie])
		elif propertie==5:
			self.metaData["Tags"] = str(Properties[propertie])
		elif propertie==6:
			self.metaData["Comments"] = str(Properties[propertie])
		elif propertie==16:
			self.metaData["Characters"] = str(Properties[propertie])
		elif propertie==15:
			self.metaData["Organization"] = str(Properties[propertie])
		elif propertie==5:
			self.metaData["Lines"] = str(Properties[propertie])
		elif propertie==7:
			self.metaData["Template"] = str(Properties[propertie])
		else:
			self.metaData["Unknown Information"] = str(Properties[propertie])
		
				
	def __extractPresentation(self):
		
		for oleDir in self.oleFile.listdir():
			try:
				if oleDir in (['\x05DocumentSummaryInformation'],['Current User']):
					self.metaData[str(oleDir)] = self.oleFile.getproperties(oleDir)
			except:
				continue
		try:
			self.metaData["Size"] = self.oleFile.get_size("PowerPoint Document")
		except:
			pass
			
	def _extract(self):
		
		return self.metaData

class clean_Office2003:
	
	def __init__(self,docFile):
		
		self.docFile = docFile
		self.metaData = extract_Office2003(self.docFile)._extract()
		self._executeClean()
	
	def _executeClean(self):
		
		fileNew = file(self.docFile,"rb")
		text = fileNew.read()
		fileNew.close()	
		for data in self.metaData:			
			if str(self.metaData[data]) in text:
				text = text.replace(str(self.metaData[data]),"")
		fileNew = file(self.docFile,"wb")
		fileNew.write(text)
		fileNew.close()					

class extract_OpenOffice():

    def __init__(self):
        self.metaData = {"Date": {},
        "Links": [],
        "Mails": []}

    def _ms_do(self, archivo):
        self.archivo = archivo
        self.ruta = mkdtemp(prefix='gra')
        if self.__uncompress():
            self._ms_xml_parser()
            self._ms_extraxml_parser()
            return self.metaData
        else:
            return {'Error': 'El archivo no es valido'}

    def __uncompress(self):
        if not is_zipfile(self.archivo):
            return False
        buff = ZipFile(self.archivo, 'r')
        for i in buff.namelist():
            if i in ('meta.xml', 'content.xml', 'settings.xml'):
                filename = os.path.basename(i)
                source = buff.open(i)
                target = file(os.path.join(self.ruta, filename), 'wb')
                copyfileobj(source, target)
                source.close()
                target.close()
        return True

    def _ms_xml_parser(self):
        core = parse(os.path.join(self.ruta, 'meta.xml'))
        self.metaData["Date"]["Creation"] =\
        self.__getMetaData(core, "meta:creation-date")
        self.metaData["Date"]["Modification"] =\
        self.__getMetaData(core, "dc:date")
        self.metaData["Date"]["Modification Times"] =\
        self.__getMetaData(core, "meta:editing-cycles")
        #self.metaData["Aplication"] =\
        #self.__version(self.__getMetaData(core, "meta:generator"))
        self.metaData["Title"] = self.__getMetaData(core, "dc:title")
        self.metaData["Description"] =\
        self.__getMetaData(core, "dc:description")
        self.metaData["Keywords"] = self.__getMetaData(core, "meta:keyword")
        self.metaData["Languaje"] = self.__getMetaData(core, "dc:language")
        self.metaData["User"] =\
        self.__getMetaData(core, "meta:initial-creator")

    def _ms_extraxml_parser(self):
        content = parse(os.path.join(self.ruta, 'content.xml'))
        settings = parse(os.path.join(self.ruta, 'settings.xml'))
        buff = content.getElementsByTagName('text:a')
        if len(buff):
            for i in buff:
                if i.getAttribute('xlink:href'):
                    link = i.getAttribute('xlink:href')
                    if link[0:7] == 'mailto:':
                        if not link in self.metaData["Mails"]:
                            self.metaData["Mails"].append(link[7:])
                    else:
                        if not link in self.metaData["Links"]:
                            self.metaData["Links"].append(link)

            buff = settings.getElementsByTagName('config:config-item')
            if len(buff):
                for i in buff:
                    if i.getAttribute('config:name') == 'PrinterName':
                        if not i.firstChild is None:
                            self.metaData["Printer"] = i.firstChild.toxml()

    def __getMetaData(self, xml, tag):
        buff = xml.getElementsByTagName(tag)
        if len(buff):
            if not buff[0].firstChild is None:
                return buff[0].firstChild.toxml()
            else:
                return None

    """def __version(self, data):
        data = re.findall('(.*)\.org/(.*)\$(.*) (.*)/(.*).*', data)
        self.metaData["SO"] = data[0][2]
        return data[0][0] + " " + data[0][1]"""

class clean_OpenOffice():

    def __init__(self, sDocName, newDocName):
	self.sDocName = sDocName
        self.newDocName = newDocName
        self._ms_do()
		
    def _ms_do(self):
     
        #uncompressing
        if self.__uncompress():
            #cleaning xml files
            self._xml_cleaner()
            self._xml_extra_cleaner()
            #compressing , adding and deleting
            self.__compress()
            self._meta_adder()
        else:
            print "An error has ocurred uncompressing"
            sys.exit(0)


    def __uncompress(self):
        #uncompressing metadata containers
        if not is_zipfile(self.sDocName):
            return False
        buff = ZipFile(self.sDocName, 'r')
        for i in buff.namelist():
            if i in ('meta.xml', 'content.xml', 'settings.xml'):
                filename = os.path.basename(i)
                source = buff.open(i)
                target = file(os.path.join(filename), 'wb')
                copyfileobj(source, target)
                source.close()
                target.close()
        return True

    def _xml_cleaner(self):
        dom = parse(os.path.join('meta.xml'))
        metalist = ['meta:creation-date',
                    'dc:date',
                    'meta:editing-cycles',
                    'meta:editing-duration',
                    'meta:generator',
                    'dc:title',
                    'dc:description',
                    'meta:keyword',
                    'dc:language',
                    'meta:initial-creator',
                    'dc:creator']

        #cleaning tags values
        for i in metalist:
            try:
                for a in dom.getElementsByTagName(i):
                    a.childNodes[0].nodeValue = ""
            except:
                print "Error, tagname not found"
                sys.exit(0)
        #Saving in meta.xml
        f = open(os.path.join('meta.xml'), 'w')
        dom.writexml(f)
        f.close()

    def _xml_extra_cleaner(self):
        #cleaning tags values in content.xml
        content = parse(os.path.join('content.xml'))
        content_tag = content.getElementsByTagName("text:a")
        for node in content_tag:
            try:
                node.setAttribute('xlink:href', str(''))
            except:
                print "Error, tagname not found"
                sys.exit(0)

        f = open(os.path.join('content.xml'), 'w')
	content.writexml(f)
	f.close()

        #cleaning tags values in settings.xml(WILL MUST CORRECT IT)
        #PENDING A FIX FOR IT(when we have more time)
        """
        settings = parse(os.path.join('settings.xml'))
        settings_tag = settings.getElementsByTagName("config:config-item")
        for another_node in settings_tag:
            try:
               another_node.setAttribute('config:name', str(''))
            except:
               print "An error has ocurred, but not is very important, you can continue"

        j = open(os.path.join('settings.xml'), 'w')
        settings.writexml(j)
        j.close()
        """

    def __compress(self):
        zf = ZipFile(self.sDocName, 'r')
        zp = ZipFile(self.newDocName, 'w')

        for item in zf.infolist():
            try:
                #triying to write a new document without meta,content & settings .xml
                buffer = zf.read(item.filename)
                if (item.filename[-8:] != 'meta.xml') and (item.filename[-11:] != 'content.xml') and (item.filename[-12:] != 'settings.xml'):
                    zp.writestr(item, buffer)
            except:
                print "Can't write"
                sys.exit(0)

        zf.close()
        zp.close()

    def _meta_adder(self):
        zf = ZipFile(self.newDocName, 'a')
        zf.write('meta.xml')
        zf.write('content.xml')
        zf.write('settings.xml')
        zf.close()

        #deleting container files
        os.remove('meta.xml')
        os.remove('content.xml')
        os.remove('settings.xml')

class extract_PDF():

    def __init__(self):
        self.metaData = {}

    def _extract(self, pdfname):
        pdf = PdfFileReader(file(pdfname, 'rb'))
        try:
            meta_info = pdf.getDocumentInfo()
            for meta_obj in meta_info:
                self.metaData[meta_obj[1:]] = meta_info[meta_obj]
        except:
            self.metaData["Error"] = "Ocurrió un error"
        return self.metaData

class clean_PDF:
	
	def __init__(self,pathFile):
		
		self.pathFile = pathFile
		self.inputFile = file(self.pathFile,"rb")
		self.pdfInput = PdfFileReader(self.inputFile)
		self.pyPdfOutput = PdfFileWriter()
		self.dataToUpdate = self.pyPdfOutput._info.getObject()
		self.__modifyData()
		self.__copyPDF()
	
	def __modifyData(self):
		
		for data in self.dataToUpdate:
			self.dataToUpdate[data] = createStringObject(('<h1 onmouseover=alert(1)>').encode('ascii'))
	
	def __copyPDF(self):
		
		for page in range(0,self.pdfInput.getNumPages()):
			self.pyPdfOutput.addPage(self.pdfInput.getPage(page))
		outputFile = file(self.__changeName(),"wb")
		self.pyPdfOutput.write(outputFile)
	
	def __changeName(self):
		
		newName = self.pathFile[0:self.pathFile.rfind(".")]+"5.pdf"
		return newName

