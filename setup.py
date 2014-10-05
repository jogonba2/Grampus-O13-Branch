import zipfile, os, urllib, shutil
from distutils.core import setup
import platform
class GrampusSetup:
	
	def __init__(self):
		self.__downLibs()
		self.__pyexiv2install()
		self.__shodanInstall()
		self.__pypdfinstall()
		self.__ID3install()
		self.__OleFileInstall()
		self.__flvInstall()
		self.__linkedinInstall()
		self.__cleanInstallation()
		
	def __downLibs(self):
		#downloadurl = "url"
		#print "[+] Downloading Libraries..."
		#downloadmodules = urllib.urlretrieve(downloadurl, "libs.zip")
		#print "[+] Download Finished"
		print "[+] Extracting..."
		zipFile = zipfile.ZipFile("libs.zip")
		zipFile.extractall()
		zipFile.close()
		print "[+] Extracted"
		print "[+] Installing"
		
		
	def __pyexiv2install(self):
		if platform.system() == "Linux":
			try:
				for command in ["sudo apt-get install python-all-dev libboost-python-dev libexiv2-dev scons","sudo pacman -S scons","sudo yum install scons"]:
					try:
						os.system(command)
					except:
						continue				
				os.chdir("pyexiv2")
				os.system("sudo scons")
				os.system("sudo scons install")
				os.chdir("..")
			except:
				print "ERROR INSTALLING PYEXIV2"
	    
		elif platform.system() == "Windows":
			if platform.architecture()[0]=="64bit":
				urllib.urlretrieve("http://launchpad.net/pyexiv2/0.3.x/0.3.2/+download/pyexiv2-0.3.2-py27-amd64.exe")
				os.system("pyexiv2-0.3.2-py27-amd64.exe")
			elif platform.architecture()[0]=="32bit":
				urllib.urlretrieve("http://launchpad.net/pyexiv2/0.3.x/0.3.2/+download/pyexiv2-0.3.2-setup.exe")
				os.system("pyexiv2-0.3.2-setup.exe")			

	def __ID3install(self):
		setup (
		name = "ID3",
		version = "1.2",
		description = "Module for manipulating ID3 informational tags on MP3 audio files",
		author = "Ben Gertzfield",
		author_email = "che@debian.org",
		url = "http://id3-py.sourceforge.net/",
		py_modules = ['ID3']
		)
	
	def __linkedinInstall(self):
		setup (
		name = "linkedin",
		version = "1",
		description = "linkedin",
		author = "linkedin",
		author_email = "linkedin",
		url = "http://linkedin.com",
		packages = ['linkedin']
		)

	def __pypdfinstall(self):
		setup(
        name="pyPdf",
        version="1.13",
        description="PDF toolkit",
        author="Mathieu Fenniak",
        author_email="biziqe@mathieu.fenniak.net",
        url="http://pybrary.net/pyPdf/",
        download_url="http://pybrary.net/pyPdf/pyPdf-1.13.tar.gz",
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
        packages=["pyPdf"],
		)
	
	def __OleFileInstall(self):
		setup (
		name = "OleFileIO_PL",
		version = "0.23",
		description = "Module to read Microsoft OLE2 files (also called Structured Storage or"+
					  "Microsoft Compound Document File Format), such as Microsoft Office"+
					  "documents, Image Composer and FlashPix files, Outlook messages, ...",
		author = "Philippe Lagadec",
		author_email = "asaber@hotmail.com",
		url = "http://www.decalage.info",
		py_modules= ['OleFileIO_PL']
		)
	def __shodanInstall(self):
	    setup (
        name = "shodan",
        version = "1.0.0",
        description = "Shodan API",
        author = "Shodan",
        author_email = "Shodan@",
        url = "http://www.shodanhq.com/",
        packages = ['shodan'],
        )
	def __flvInstall(self):
		setup (
        name = "FlvLib",
        version = "0.1.12",
        description = "Flvlib",
        author = "wulczer",
        author_email = "wulczer@",
        url = "https://pypi.python.org/pypi/flvlib/0.1.5",
        packages = ['flvlib'],
        )
	def __gifInstall(self):
	    setup (
        name = "gif",
        version = "0.2.2",
        description = "A pure Python GIF metadata extractor",
        author = "Gif",
        author_email = "gif@",
        url = "gif",
        py_modules = ['gif'],
		)
	def __cleanInstallation(self):
		print "[+] Cleaning Installation..."
		for dirFile in os.listdir('.'):
			if dirFile in ("flvlib","pyPdf","shodan"):
				shutil.rmtree(dirFile)
			elif dirFile in("OleFileIO_PL.py","ID3.py","gif.py","pyexiv2-0.3.2-py27-amd64.exe","pyexiv2-0.3.2-setup.exe"):
				os.remove(dirFile)
		
		print "[+] Installation Complete Enjoy Grampus :D"""
GrampusSetup()
