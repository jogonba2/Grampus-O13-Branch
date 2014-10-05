from PyQt4 import QtGui, QtCore
import sys
import Grampus
class WindowGrampus(QtGui.QMainWindow,Grampus.GUI):
	
	def __init__(self):
		super(WindowGrampus,self).__init__()
		self.__setPropertyMainWindow()
		self.__setMenuToolbar()
		self.__setActionsMenu()
		self.__actionConnections()
		self.centralWidget = Grampus.GUI()
		self.centralWidget._setStatusBar(self.statusBar())
		self.setCentralWidget(self.centralWidget) # Usamos GUI como widget central en el MainWindow
		self.show()
		
	# Define Los Atributos Del MainWindow
	def __setPropertyMainWindow(self):
		
		self.setWindowTitle("Grampus Beta")
		self.setWindowIcon(QtGui.QIcon("recursos/icon.jpg"))
		self.resize(900,300)
		self.setAcceptDrops(True)
		self.sBar = QtGui.QStatusBar()
		self.sBar.setFixedHeight(10)
		self.setStatusBar(self.sBar)
	
	# Define Las Propiedades Del MenuBar
	def __setMenuToolbar(self):
		
		# Menus de prueba
		self.bar = self.menuBar()
		self.grampus = self.bar.addMenu("&Grampus")
		#self.forensicGrampus = self.bar.addMenu("&Forensic-Grampus")
	
	# Define Actions Del MenuBar
	def __setActionsMenu(self):
		
		self.actionSave = QtGui.QAction("Save",self)
		self.actionSaveAll = QtGui.QAction("Save All",self)
		#self.actionDonate = QtGui.QAction("Donate",self)
		#self.actionContact = QtGui.QAction("Contact",self)
		self.actionClose = QtGui.QAction("Close",self)
		self.actionClose.triggered.connect(QtGui.qApp.quit)
		self.grampus.addAction(self.actionSave)
		self.grampus.addAction(self.actionSaveAll)
		#self.grampus.addAction(self.actionDonate)
		#self.grampus.addAction(self.actionContact)
		self.grampus.addAction(self.actionClose)
	
	def __actionConnections(self):
		self.actionSave.triggered.connect(self.__saveActualData)
		self.actionSaveAll.triggered.connect(self.__saveAllData)
	
	def __saveActualData(self):
		tabWidget = self.centralWidget._returnTab2Save()
		if tabWidget.count()>0:
			self.statusBar().showMessage(self.tr("Saving:" + tabWidget.tabText(tabWidget.currentIndex())))
			tabName = str(tabWidget.tabText(tabWidget.currentIndex()))
			tabText = str(tabWidget.widget(tabWidget.currentIndex()).toPlainText().toUtf8)
			fileName = tabName[0:tabName.rfind('.')]+".txt"
			file2Save = open("saves/"+fileName,"w")
			file2Save.write("------ " + tabName + " ------\r\n\r\n")
			file2Save.write(tabText)
			file2Save.close()
			self.statusBar().showMessage("Saved: " + self.tr(tabWidget.tabText(tabWidget.currentIndex())))
			
	
	def __saveAllData(self):
		tabWidget = self.centralWidget._returnTab2Save()
		if tabWidget.count()>0:
			self.statusBar().showMessage(self.tr("Saving All"))
			for i in range(0,tabWidget.count()):
				tabName = str(tabWidget.tabText(i))
				tabText = str(tabWidget.widget(i).toPlainText().toUtf8)
				fileName = tabName[0:tabName.rfind('.')]+".txt"
				file2Save = open("saves/"+fileName,'a')
				file2Save.write("------ " + tabName + " ------\r\n\r\n")
				file2Save.write(tabText)
				file2Save.write("\r\n\r\n")
				file2Save.close()
			self.statusBar().showMessage(self.tr("All Saved"))
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	guiGrampus = WindowGrampus()
	app.exec_()
