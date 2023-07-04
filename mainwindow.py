from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("WaveDiffQT")
        self.resize(1600, 1000)


        #global settings
        self.wavelength = 532.8
        self.xin = 2500
        self.yin = 2500

        self.xout = 500
        self.yout = 500

        self.use3Dforcalculating = False

        self.makeWidgets()
        self.makeMenuBar()
        self.addItems()

        self.showGlobalSettings()

        
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

        self.layout.addLayout(self.componentsLayout, 15)

        self.schemeWidget = QtWidgets.QWidget()
        self.schemeWidget.setStyleSheet("background: gray")
        self.layout.addWidget(self.schemeWidget, 70)

        self.dataWidget = QtWidgets.QWidget()
        self.dataWidget.setStyleSheet("background: white; border: 1px solid gray")
        self.layout.addWidget(self.dataWidget, 15)

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

        self.globalSettingsButton = QtWidgets.QAction("&Globalne nastavitve...")
        self.globalSettingsButton.triggered.connect(self.showGlobalSettings)
        self.settingsMenu.addAction(self.globalSettingsButton)

    def showGlobalSettings(self):
        globalSettingsLayout = QtWidgets.QVBoxLayout()

        wavelengthLayout = QtWidgets.QHBoxLayout()
        wavelengthLabel = QtWidgets.QLabel()
        wavelengthLabel.setText("Valovna dolžina:")
        wavelengthLabel.setStyleSheet("border: none")

        wavelengthLineEdit = QtWidgets.QLineEdit()
        wavelengthLineEdit.setValidator(QtGui.QIntValidator())
        wavelengthLineEdit.setText(str(self.wavelength))
        wavelengthLineEdit.textChanged.connect(lambda w: print(w))

        wavelengthLayout.addWidget(wavelengthLabel)
        wavelengthLayout.addWidget(wavelengthLineEdit)

        globalSettingsLayout.addLayout(wavelengthLayout)
        
        inputLayout = QtWidgets.QVBoxLayout()
        xinLayout = QtWidgets.QHBoxLayout()
        yinLayout = QtWidgets.QHBoxLayout()

        xinLabel = QtWidgets.QLabel()
        xinLabel.setText("Velikost vhodnega x-polja:")
        xinLabel.setStyleSheet("border: none")
        
        xinLineEdit = QtWidgets.QLineEdit()
        xinLineEdit.setValidator(QtGui.QIntValidator())
        xinLineEdit.setText(str(self.xin))
        xinLineEdit.textChanged.connect(lambda xin: print(xin))

        xinLayout.addWidget(xinLabel)
        xinLayout.addWidget(xinLineEdit)
        inputLayout.addLayout(xinLayout)

        yinLabel = QtWidgets.QLabel()
        yinLabel.setText("Velikost vhodnega y-polja:")
        yinLabel.setStyleSheet("border: none")
        
        yinLineEdit = QtWidgets.QLineEdit()
        yinLineEdit.setValidator(QtGui.QIntValidator())
        yinLineEdit.setText(str(self.yin))
        yinLineEdit.textChanged.connect(lambda yin: print(yin))

        yinLayout.addWidget(yinLabel)
        yinLayout.addWidget(yinLineEdit)
        inputLayout.addLayout(yinLayout)

        globalSettingsLayout.addLayout(inputLayout)

        outputLayout = QtWidgets.QVBoxLayout()
        xoutLayout = QtWidgets.QHBoxLayout()
        youtLayout = QtWidgets.QHBoxLayout()

        xoutLabel = QtWidgets.QLabel()
        xoutLabel.setText("Velikost izhodnega x-polja:")
        xoutLabel.setStyleSheet("border: none")
        
        xoutLineEdit = QtWidgets.QLineEdit()
        xoutLineEdit.setValidator(QtGui.QIntValidator())
        xoutLineEdit.setText(str(self.xout))
        xoutLineEdit.textChanged.connect(lambda xout: print(xout))

        xoutLayout.addWidget(xoutLabel)
        xoutLayout.addWidget(xoutLineEdit)
        outputLayout.addLayout(xoutLayout)

        youtLabel = QtWidgets.QLabel()
        youtLabel.setText("Velikost izhodnega y-polja:")
        youtLabel.setStyleSheet("border: none")
        
        youtLineEdit = QtWidgets.QLineEdit()
        youtLineEdit.setValidator(QtGui.QIntValidator())
        youtLineEdit.setText(str(self.yout))
        youtLineEdit.textChanged.connect(lambda yout: print(yout))

        youtLayout.addWidget(youtLabel)
        youtLayout.addWidget(youtLineEdit)
        outputLayout.addLayout(youtLayout)

        globalSettingsLayout.addLayout(outputLayout)

        czt3DLayout = QtWidgets.QHBoxLayout()
        czt3dLabel = QtWidgets.QLabel()
        czt3dLabel.setText("Uporabi 3D za izračun:")
        czt3dLabel.setStyleSheet("border: none")

        czt3dCheckBox = QtWidgets.QCheckBox()
        czt3dCheckBox.setChecked(self.use3Dforcalculating)
        czt3dCheckBox.setStyleSheet("border: none")

        czt3DLayout.addWidget(czt3dLabel)
        czt3DLayout.addWidget(czt3dCheckBox)
        globalSettingsLayout.addLayout(czt3DLayout)

        self.dataWidget.setLayout(globalSettingsLayout)

    def addItems(self):
        self.sourcesListWidget.addItem("Ravno valovanje")
        self.sourcesListWidget.addItem("Sferično valovanje")
        self.sourcesListWidget.addItem("Gaussov snop")

        self.masksListWidget.addItem("Maska")
        self.masksListWidget.addItem("Leča")
        self.masksListWidget.addItem("Difraktična leča")
        self.masksListWidget.addItem("Aksionska leča")
        self.masksListWidget.addItem("Prizma")
        self.masksListWidget.addItem("Slika")
