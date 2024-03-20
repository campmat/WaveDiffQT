from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import matplotlib.pyplot as plt
import inspect
import json
import math

from diffractio.scalar_sources_XY import Scalar_source_XY
from diffractio.scalar_masks_XY import Scalar_mask_XY

from opticalobject import OpticalObject

from maskeditor import MaskEditor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("WaveDiffQT")
        self.resize(1600, 1000)

        #file settings
        self.fileName = None

        #global settings
        self.wavelength = 532.8
        self.xin = 2500
        self.yin = 2500

        self.xout = 500
        self.yout = 500

        self.use3Dforcalculating = False
        self.max_z = 1000

        self.N = 2048

        self.currentZ = 0

        #optical objects
        self.selected_new_object = None
        self.new_object = None
        self.new_object_data = None
        self.new_object_type = None
        self.new_object_func = None
        self.optical_objects = []

        self.maskEditor = MaskEditor(self)

        self.makeWidgets()
        self.makeMenuBar()
        self.addItems()

        self.showGlobalSettings()
        
    def newFile(self):
        self.fileName = None
        self.optical_objects = []

        self.wavelength = 532.8
        self.xin = 2500
        self.yin = 2500

        self.xout = 500
        self.yout = 500

        self.use3Dforcalculating = False
        self.cut_value = 0.0025
        self.max_z = 1000
        self.N = 2048

    def openFile(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setNameFilter("*.json")
        fileDialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        fileDialog.setWindowTitle("Odpri datoteko")

        if fileDialog.exec_():
            self.fileName = fileDialog.selectedFiles()[0]
            file = open(self.fileName, "r")
            data = json.load(file)
            file.close()

            self.wavelength = data["wavelength"]
            self.xin = data["xin"]
            self.yin = data["yin"]

            self.xout = data["xout"]
            self.yout = data["yout"]

            self.use3Dforcalculating = data["use3Dforcalculating"]
            self.max_z = data["max_z"]
            self.N = data["N"]

            for optical_obj_data in data["optical_objects"]:
                #print(optical_obj_data)
                xfield = np.linspace(-self.xin, self.xin, self.N)
                yfield = np.linspace(-self.yin, self.yin, self.N)
                new_object = None
                if optical_obj_data["type"] == "source":
                    new_object = Scalar_source_XY(xfield, yfield, self.wavelength)
                
                    if optical_obj_data["func"] == "plane_wave":
                        new_object.plane_wave(*optical_obj_data["data"])
                    elif optical_obj_data["func"] == "spherical_wave":
                        new_object.spherical_wave(*optical_obj_data["data"])
                    elif optical_obj_data["func"] == "gauss_beam":
                        new_object.gauss_beam(*optical_obj_data["data"])
                
                elif optical_obj_data["type"] == "mask":
                    new_object = Scalar_mask_XY(xfield, yfield, self.wavelength)
                    if optical_obj_data["func"] == "mask":
                        new_object = self.maskEditor.makeMaskFromShapeList(optical_obj_data["data"])
                            
                    elif optical_obj_data["func"] == "lens":
                        new_object.lens(*optical_obj_data["data"])
                    elif optical_obj_data["func"] == "fresnel_lens":
                        new_object.fresnel_lens(*optical_obj_data["data"])
                    elif optical_obj_data["func"] == "axicon":
                        new_object.axicon(*optical_obj_data["data"])
                            
                self.optical_objects.append(OpticalObject(optical_obj_data["name"], optical_obj_data["pozZ"], optical_obj_data["data"], optical_obj_data["type"], optical_obj_data["func"], new_object))

            self.showGlobalSettings()

    def saveFile(self):
        if self.fileName == None:
            self.saveFileAs()
        else:
            optical_objects_data = []
            for optical_obj in self.optical_objects:
                optical_objects_data.append(optical_obj.toJSON())

            data = {}

            data["wavelength"] = self.wavelength
            data["xin"] = self.xin
            data["yin"] = self.yin
            data["xout"] = self.xout
            data["yout"] = self.yout
            data["use3Dforcalculating"] = self.use3Dforcalculating
            data["max_z"] = self.max_z
            data["N"] = self.N
            data["optical_objects"] = optical_objects_data

            file = open(self.fileName, "w")
            file.write(json.dumps(data))
            file.close()

    def saveFileAs(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setNameFilter("*.json")
        fileDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fileDialog.setWindowTitle("Shrani datoteko kot ...")
        fileDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        if fileDialog.exec_():
            self.fileName = fileDialog.selectedFiles()[0]
            if self.fileName.split(".")[-1].lower() != "json":
                self.fileName = self.fileName + ".json"
            
            self.saveFile()
        
    def openSettings(self):
        print("Nastavitve")

    def updateZSelectorAndLineEdit(self):
        self.zSelector.setValue(self.currentZ)
        self.zLineEdit.setText(str(self.currentZ))

    def onZSelectorChange(self):
        self.currentZ = self.zSelector.value()
        self.updateZSelectorAndLineEdit()

    def onZLineEditChange(self):
        self.currentZ = int(self.zLineEdit.text())
        self.updateZSelectorAndLineEdit()

    def showDiffraction(self):
        if self.use3Dforcalculating:
            pass
        else:
            zPoz = self.zSelector.value()
            self.optical_objects = sorted(self.optical_objects, key=lambda x : x.pozZ)

            u = None

            for opticalobj in self.optical_objects:
                if u == None:
                    u = opticalobj.obj
                    continue
                if opticalobj.pozZ <= zPoz:
                    oldU = u
                    u = u.CZT(opticalobj.pozZ, self.xout, self.yout)
                    oldU.u = u
                    u = oldU
                    
                    if opticalobj.type == "mask":
                        u = opticalobj.obj * u                

            u.draw(logarithm = True)
            plt.show()

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

        schemeLayout = QtWidgets.QVBoxLayout()

        self.schemeWidget = QtWidgets.QWidget()
        self.schemeWidget.setStyleSheet("background: gray")
        schemeLayout.addWidget(self.schemeWidget)

        self.zSelector = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.zLineEdit = QtWidgets.QLineEdit()        
        showBtn = QtWidgets.QPushButton("Prikaži")
        self.zSelector.setMaximum(self.max_z)

        self.updateZSelectorAndLineEdit()
        self.zSelector.valueChanged.connect(self.onZSelectorChange)
        self.zLineEdit.returnPressed.connect(self.onZLineEditChange)

        showBtn.clicked.connect(self.showDiffraction)

        zQVBoxLayout = QtWidgets.QVBoxLayout()
        zQHBoxLayout = QtWidgets.QHBoxLayout()

        zQVBoxLayout.addWidget(self.zSelector)
        zQHBoxLayout.addWidget(self.zLineEdit, 10)
        zQHBoxLayout.addWidget(showBtn, 10)
        zQVBoxLayout.addLayout(zQHBoxLayout)

        schemeLayout.addLayout(zQVBoxLayout)
        self.layout.addLayout(schemeLayout, 70)

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
        self.saveFileAsButton.setShortcut(QtGui.QKeySequence("Ctrl+Shift+s"))
        self.fileMenu.addAction(self.saveFileAsButton)

        self.settingsMenu = self.menu.addMenu("&Nastavitve")

        self.settingsButton = QtWidgets.QAction("&Nastavitve ...")
        self.settingsButton.triggered.connect(self.openSettings)
        self.settingsMenu.addAction(self.settingsButton)

        self.globalSettingsButton = QtWidgets.QAction("&Globalne nastavitve...")
        self.globalSettingsButton.setShortcut(QtGui.QKeySequence("Ctrl+g"))
        self.globalSettingsButton.triggered.connect(self.showGlobalSettings)
        self.settingsMenu.addAction(self.globalSettingsButton)

        self.opticalObjectsButton = QtWidgets.QAction("&Optični objekti")
        self.opticalObjectsButton.triggered.connect(self.showOpticalObjects)
        self.settingsMenu.addAction(self.opticalObjectsButton)

    def setXin(self):
        new_xin = float(self.sender().text())
        if new_xin != None:
            self.xin = new_xin

    def setXout(self):
        new_xout = float(self.sender().text())
        if new_xout != None:
            self.xout = new_xout

    def setYin(self):
        new_yin = float(self.sender().text())
        if new_yin != None:
            self.yin = new_yin
    
    def setYout(self):
        new_yout = float(self.sender().text())
        if new_yout != None:
            self.yout = new_yout

    def setWavelength(self):
        new_wavelength = float(self.sender().text())
        if new_wavelength != None:
            self.wavelength = new_wavelength

    def setMaxZ(self):
        new_max_z = float(self.sender().text())
        if new_max_z != None:
            self.max_z = new_max_z

    def setCZT3D(self):
        new_czt3d = self.sender().isChecked()
        if new_czt3d != None:
            if new_czt3d:
                self.use3Dforcalculating = True
            else:
                self.use3Dforcalculating = False

    def setN(self):
        new_N = float(self.sender().text())
        if new_N != None:
            if math.ceil(math.log2(new_N)) != math.floor(math.log2(new_N)):
                new_N = 2 ** math.floor(math.log2(new_N))
            self.N = new_N
            self.showGlobalSettings()

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

        Nlayout = self.makeHBoxLayoutWithLabelAndLineEdit("Število točk:", self.N, self.setN)
        globalSettingsLayout.addLayout(Nlayout)

        czt3DLayout = self.makeHBoxLayoutWithLabelAndCheckBox("Uporabi 3D za izračun:", self.use3Dforcalculating, self.setCZT3D)
        globalSettingsLayout.addLayout(czt3DLayout)

        if self.dataWidget.layout() != None:
            QtWidgets.QWidget().setLayout(self.dataWidget.layout())
        self.dataWidget.setLayout(globalSettingsLayout)

    def opticalElementProperties(self, item):
        self.selected_new_object = item.text()
        self.addItemLayout = QtWidgets.QVBoxLayout()
        signature = None

        xfield = np.linspace(-self.xin, self.xin, self.N)
        yfield = np.linspace(-self.yin, self.yin, self.N)

        if item.text() == "Ravno valovanje":
            self.new_object = Scalar_source_XY(xfield, yfield, self.wavelength)
            self.new_object_type = "source"
            self.new_object_func = "plane_wave"
            signature = self.get_default_args(self.new_object.plane_wave)                
        elif item.text() == "Sferično valovanje":
            self.new_object = Scalar_source_XY(xfield, yfield, self.wavelength)
            self.new_object_type = "source"
            self.new_object_func = "spherical_wave"
            signature = self.get_default_args(self.new_object.spherical_wave) 
        elif item.text() == "Gaussov snop":
            self.new_object = Scalar_source_XY(xfield, yfield, self.wavelength)
            self.new_object_type = "source"
            self.new_object_func = "gauss_beam"
            signature = self.get_default_args(self.new_object.gauss_beam) 
        elif item.text() == "Maska":
            self.maskEditor.show()
            self.new_object_type = "mask"
            self.new_object_func = "mask"
            return
        elif item.text() == "Leča":
            self.new_object = Scalar_mask_XY(xfield, yfield, self.wavelength)
            self.new_object_type = "mask"
            self.new_object_func = "lens"
            signature = self.get_default_args(self.new_object.lens)
        elif item.text() == "Difraktična leča":
            self.new_object = Scalar_mask_XY(xfield, yfield, self.wavelength)
            self.new_object_type = "mask"
            self.new_object_func = "fresnel_lens"
            signature = self.get_default_args(self.new_object.fresnel_lens)
        elif item.text() == "Aksionska leča":
            self.new_object = Scalar_mask_XY(xfield, yfield, self.wavelength)
            self.new_object_type = "mask"
            self.new_object_func = "axicon"
            signature = self.get_default_args(self.new_object.axicon)
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
                initial_val = 0
                if arg == "w0":
                    initial_val = 1  
                layoutX = self.makeHBoxLayoutWithLabelAndLineEdit(arg + "_x", initial_val, None)
                layoutY = self.makeHBoxLayoutWithLabelAndLineEdit(arg + "_y", initial_val, None)
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

        self.new_object_data = data
        #print(*data)

        if self.selected_new_object == "Ravno valovanje":
            self.new_object.plane_wave(*data)                
        elif self.selected_new_object == "Sferično valovanje":
            self.new_object.spherical_wave(*data) 
        elif self.selected_new_object == "Gaussov snop":
            self.new_object.gauss_beam(*data)
        elif self.selected_new_object == "Maska":
            self.new_object_data = self.maskEditor.shapes
            self.new_object = self.maskEditor.mask
        elif self.selected_new_object == "Leča":
            self.new_object.lens(*data)
        elif self.selected_new_object == "Difraktična leča":
            self.new_object.fresnel_lens(*data)
        elif self.selected_new_object == "Aksionska leča":
            self.new_object.axicon(*data)
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
        
        self.optical_objects.append(OpticalObject(name, pozZ, self.new_object_data, self.new_object_type, self.new_object_func, self.new_object))
        self.selected_new_object = None
        self.new_object = None
        self.new_object_data = None
        self.new_object_type = None
        self.new_object_func = None
        self.showGlobalSettings()

    def showOpticalObjects(self):
        layout = QtWidgets.QVBoxLayout()

        for optical_obj in self.optical_objects:
            obj_layout = QtWidgets.QVBoxLayout()
            arg_layout = QtWidgets.QHBoxLayout()
            data_layout = QtWidgets.QHBoxLayout()

            name_label = QtWidgets.QLabel()
            name_label.setText(optical_obj.name)
            name_label.setStyleSheet("border: none")

            poz_z_label = QtWidgets.QLabel()
            poz_z_label.setText(str(optical_obj.pozZ))
            poz_z_label.setStyleSheet("border: none")

            data_label = QtWidgets.QLabel()
            data_label.setText(str(optical_obj.data))
            data_label.setStyleSheet("border: none")

            arg_layout.addWidget(name_label)
            arg_layout.addWidget(poz_z_label)
            data_layout.addWidget(data_label)

            obj_layout.addLayout(arg_layout)
            obj_layout.addLayout(data_layout)
            layout.addLayout(obj_layout)

        if self.dataWidget.layout() != None:
            QtWidgets.QWidget().setLayout(self.dataWidget.layout())
        self.dataWidget.setLayout(layout)

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
            lineEdit.editingFinished.connect(callback_func)

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

    def closeEvent(self, event):
        if self.maskEditor:
            self.maskEditor.close()
        
        event.accept()