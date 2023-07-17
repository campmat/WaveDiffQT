from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import inspect

from diffractio.scalar_sources_XY import Scalar_source_XY

from opticalobject import OpticalObject

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

        self.max_z = 1000

        #optical objects
        self.selected_new_object = None
        self.new_object = None
        self.optical_objects = []

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

        self.sourcesListWidget.itemActivated.connect(self.opticalElementProperties)
        self.masksListWidget.itemActivated.connect(self.opticalElementProperties)

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
        self.globalSettingsButton.setShortcut(QtGui.QKeySequence("Ctrl+g"))
        self.globalSettingsButton.triggered.connect(self.showGlobalSettings)
        self.settingsMenu.addAction(self.globalSettingsButton)

    def setXin(self, new_xin):
        if new_xin != None:
            self.xin = new_xin

    def setXout(self, new_xout):
        if new_xout != None:
            self.xout = new_xout

    def setYin(self, new_yin):
        if new_yin != None:
            self.yin = new_yin
    
    def setYout(self, new_yout):
        if new_yout != None:
            self.yout = new_yout

    def setWavelength(self, new_wavelength):
        if new_wavelength != None:
            self.wavelength = new_wavelength

    def setMaxZ(self, new_max_z):
        if new_max_z != None:
            self.max_z = new_max_z

    def setCZT3D(self, new_czt3d):
        if new_czt3d != None:
            if new_czt3d:
                self.use3Dforcalculating = True
            else:
                self.use3Dforcalculating = False

    def showGlobalSettings(self):
        globalSettingsLayout = QtWidgets.QVBoxLayout()

        wavelengthLayout = self.makeHBoxLayoutWithLabelAndLineEdit("Valovna dolžina:", self.wavelength, self.setWavelength)
        globalSettingsLayout.addLayout(wavelengthLayout)
        
        inputLayout = QtWidgets.QVBoxLayout()
        xinLayout = self.makeHBoxLayoutWithLabelAndLineEdit("Velikost vhodnega x-polja:", self.xin, self.setXin)
        yinLayout = self.makeHBoxLayoutWithLabelAndLineEdit("Velikost vhodnega y-polja:", self.yin, self.setYin)
        inputLayout.addLayout(xinLayout)
        inputLayout.addLayout(yinLayout)
        globalSettingsLayout.addLayout(inputLayout)

        outputLayout = QtWidgets.QVBoxLayout()
        xoutLayout = self.makeHBoxLayoutWithLabelAndLineEdit("Velikost izhodnega x-polja:", self.xout, self.setXout)
        youtLayout = self.makeHBoxLayoutWithLabelAndLineEdit("Velikost izhodnega y-polja:", self.yout, self.setYout)
        outputLayout.addLayout(xoutLayout)
        outputLayout.addLayout(youtLayout)
        globalSettingsLayout.addLayout(outputLayout)

        maxZLayout = self.makeHBoxLayoutWithLabelAndLineEdit("Maksimalni z:", self.max_z, self.setMaxZ)
        globalSettingsLayout.addLayout(maxZLayout)

        czt3DLayout = self.makeHBoxLayoutWithLabelAndCheckBox("Uporabi 3D za izračun:", self.use3Dforcalculating, self.setCZT3D)
        globalSettingsLayout.addLayout(czt3DLayout)

        if self.dataWidget.layout() != None:
            QtWidgets.QWidget().setLayout(self.dataWidget.layout())
        self.dataWidget.setLayout(globalSettingsLayout)

    def opticalElementProperties(self, item):
        self.selected_new_object = item.text()
        self.addItemLayout = QtWidgets.QVBoxLayout()
        signature = None
        if item.text() == "Ravno valovanje":
            self.new_object = Scalar_source_XY(self.xin, self.yin, self.wavelength)
            signature = self.get_default_args(self.new_object.plane_wave)                
        elif item.text() == "Sferično valovanje":
            self.new_object = Scalar_source_XY(self.xin, self.yin, self.wavelength)
            signature = self.get_default_args(self.new_object.spherical_wave) 
        elif item.text() == "Gaussov snop":
            self.new_object = Scalar_source_XY(self.xin, self.yin, self.wavelength)
            signature = self.get_default_args(self.new_object.gauss_beam) 
        elif item.text() == "Maska":
            pass
        elif item.text() == "Leča":
            pass
        elif item.text() == "Difraktična leča":
            pass
        elif item.text() == "Aksionska leča":
            pass
        elif item.text() == "Prizma":
            pass
        elif item.text() == "Slika":
            pass
        else:
            print(item.text())

        #print(signature)
        for arg in signature:
            layout = None
            if type(signature[arg]) == int or type(signature[arg]) == float:
                layout = self.makeHBoxLayoutWithLabelAndLineEdit(arg, signature[arg], None)
            elif type(signature[arg]) == bool:
                layout = self.makeHBoxLayoutWithLabelAndCheckBox(arg, signature[arg], None)
            else:
                layout = QtWidgets.QHBoxLayout()
                layoutX = self.makeHBoxLayoutWithLabelAndLineEdit(arg + "_x", 0, None)
                layoutY = self.makeHBoxLayoutWithLabelAndLineEdit(arg + "_x", 0, None)
                layout.addLayout(layoutX)
                layout.addLayout(layoutY)
            self.addItemLayout.addLayout(layout)

        submitBtn = QtWidgets.QPushButton()
        submitBtn.setText("Potrdi!")
        submitBtn.clicked.connect(self.setOpticalElementProperties)

        self.addItemLayout.addWidget(submitBtn)

        if self.dataWidget.layout() != None:
            QtWidgets.QWidget().setLayout(self.dataWidget.layout())
        self.dataWidget.setLayout(self.addItemLayout)

    def setOpticalElementProperties(self):
        data = []

        for child in self.addItemLayout.children():
            if len(child.children()) == 2: #x,y fields
                subData = []
                for j in range(child.count()):
                    for i in range(child.itemAt(j).count()):
                        item = child.itemAt(j).itemAt(i).widget()
                        if type(item) == QtWidgets.QLineEdit:
                            subData.append(float(item.text()))
                data.append(subData)
            else:
                for i in range(child.count()):
                    item = child.itemAt(i).widget()
                    if type(item) == QtWidgets.QLineEdit:
                        data.append(float(item.text()))

        #print(*data)

        if self.selected_new_object == "Ravno valovanje":
            self.new_object.plane_wave(*data)                
        elif self.selected_new_object == "Sferično valovanje":
            self.new_object.spherical_wave(*data) 
        elif self.selected_new_object == "Gaussov snop":
            self.new_object.gauss_beam(*data)
        elif self.selected_new_object == "Maska":
            pass
        elif self.selected_new_object == "Leča":
            pass
        elif self.selected_new_object == "Difraktična leča":
            pass
        elif self.selected_new_object == "Aksionska leča":
            pass
        elif self.selected_new_object == "Prizma":
            pass
        elif self.selected_new_object == "Slika":
            pass
        else:
            print(item.text())
        
        opticalObjectLayout = QtWidgets.QVBoxLayout()
        
        nameLayout = self.makeHBoxLayoutWithLabelAndLineEdit("Ime objekta:", "", None, False)
        opticalObjectLayout.addLayout(nameLayout)

        zPozLayout = self.makeHBoxLayoutWithLabelAndLineEdit("z-pozicija objekta:", "", None)
        opticalObjectLayout.addLayout(zPozLayout)

        submitBtn = QtWidgets.QPushButton()
        submitBtn.setText("Dodaj!")
        submitBtn.clicked.connect(self.addOpticalElement)
        opticalObjectLayout.addWidget(submitBtn)

        if self.dataWidget.layout() != None:
            QtWidgets.QWidget().setLayout(self.dataWidget.layout())
        self.dataWidget.setLayout(opticalObjectLayout)

    def addOpticalElement(self):
        layout = self.dataWidget.layout()
        name = None
        pozZ = 0
        for child in layout.children():
            for i in range(child.count()):
                item = child.itemAt(i).widget()
                if i > 0:
                    if name == None:
                        name = item.text()
                    else:
                        pozZ = float(item.text())
        
        self.optical_objects.append(OpticalObject(name, pozZ, self.new_object))
        self.selected_new_object = None
        self.new_object = None
        self.showGlobalSettings()

    def makeHBoxLayoutWithLabelAndLineEdit(self, label_text, initial_value, callback_func, intValidator=True):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel()
        label.setText(label_text)
        label.setStyleSheet("border: none")
    
        lineEdit = QtWidgets.QLineEdit()
        if intValidator:
            lineEdit.setValidator(QtGui.QIntValidator())
        if type(initial_value) != str:
            initial_value = str(initial_value)

        lineEdit.setText(initial_value)
        if callback_func != None:
            lineEdit.textChanged.connect(callback_func)

        layout.addWidget(label)
        layout.addWidget(lineEdit)

        return layout
    
    def makeHBoxLayoutWithLabelAndCheckBox(self, label_text, inital_value, callback_func):
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel()
        label.setText(label_text)
        label.setStyleSheet("border: none")

        checkBox = QtWidgets.QCheckBox()
        checkBox.setChecked(inital_value)
        
        checkBox.setStyleSheet("border: none")
        if callback_func != None:
            checkBox.stateChanged.connect(callback_func)

        layout.addWidget(label)
        layout.addWidget(checkBox)
        
        return layout
    
    def get_default_args(self, func):
        signature = inspect.signature(func)
        return {
            k: v.default
            for k, v in signature.parameters.items()
        }

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
