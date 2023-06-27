from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("WaveDiffQT")
        self.resize(1600, 1000)

        self.makeWidgets()
        self.makeMenuBar()
        self.addItems()

        
    def newFile(self):
        print("Nova datoteka")

    def openFile(self):
        print("Odpri datoteko")

    def saveFile(self):
        print("Shrani datoteko")

    def saveFileAs(self):
        print("Shrani datoteko kot")
        
    def openSettings(self):
        print("Nastavitve")
        
    def makeWidgets(self):
        self.layout = QtWidgets.QHBoxLayout()

        self.componentsLayout = QtWidgets.QVBoxLayout()

        self.sourcesListWidget = QtWidgets.QListWidget()
        self.componentsLayout.addWidget(self.sourcesListWidget)
        self.masksListWidget = QtWidgets.QListWidget()
        self.componentsLayout.addWidget(self.masksListWidget)

        self.layout.addLayout(self.componentsLayout, 25)

        self.schemeWidget = QtWidgets.QWidget()
        self.schemeWidget.setStyleSheet("background: gray")
        self.layout.addWidget(self.schemeWidget, 50)

        self.dataWidget = QtWidgets.QWidget()
        self.dataWidget.setStyleSheet("background: white; border: 1px solid gray")
        self.layout.addWidget(self.dataWidget, 25)

        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)
    
    def makeMenuBar(self):
        self.menu = self.menuBar()

        self.fileMenu = self.menu.addMenu("&Datoteka")

        self.newFileButton = QtWidgets.QAction("&Nova datoteka")
        self.newFileButton.triggered.connect(self.newFile)
        self.newFileButton.setShortcut(QtGui.QKeySequence("Ctrl+n"))
        self.fileMenu.addAction(self.newFileButton)

        self.openFileButton = QtWidgets.QAction("&Odpri datoteko")
        self.openFileButton.triggered.connect(self.openFile)
        self.openFileButton.setShortcut(QtGui.QKeySequence("Ctrl+o"))
        self.fileMenu.addAction(self.openFileButton)

        self.fileMenu.addSeparator()

        self.saveFileButton = QtWidgets.QAction("&Shrani datoteko")
        self.saveFileButton.triggered.connect(self.saveFile)
        self.saveFileButton.setShortcut(QtGui.QKeySequence("Ctrl+s"))
        self.fileMenu.addAction(self.saveFileButton)

        self.saveFileAsButton = QtWidgets.QAction("Shrani datoteko &kot")
        self.saveFileAsButton.triggered.connect(self.saveFileAs)
        self.saveFileAsButton.setShortcut(QtGui.QKeySequence("Ctrl+Alt+s"))
        self.fileMenu.addAction(self.saveFileAsButton)

        self.settingsMenu = self.menu.addMenu("&Nastavitve")

        self.settingsButton = QtWidgets.QAction("&Nastavitve ...")
        self.settingsButton.triggered.connect(self.openSettings)
        self.settingsMenu.addAction(self.settingsButton)

    def addItems(self):
        self.sourcesListWidget.addItem("Ravno valovanje")
        self.sourcesListWidget.addItem("Sferično valovanje")
        self.sourcesListWidget.addItem("Gaussov snop")