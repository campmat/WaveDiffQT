from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import math
import json

from diffractio.scalar_masks_XY import Scalar_mask_XY

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

class LineEditWithLabel(QtWidgets.QWidget):
    def __init__(self, label_text, default_val):
        super().__init__()
        self.label_text = label_text
        self.default_val = default_val

        self.label = QtWidgets.QLabel(self.label_text)
        self.line_edit = QtWidgets.QLineEdit(str(self.default_val))

        self.label.setStyleSheet("border: none")
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.setLayout(layout)
class MaskEditor(QtWidgets.QMainWindow):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        xfield = np.linspace(-self.mainwindow.xin, self.mainwindow.xin, self.mainwindow.N)
        yfield = np.linspace(-self.mainwindow.yin, self.mainwindow.yin, self.mainwindow.N)
        self.mask = Scalar_mask_XY(xfield, yfield, self.mainwindow.wavelength)

        self.setWindowTitle("Mask Editor")
        self.resize(1600, 1000)

        self.fileName = None
        self.shapes = []

        self.plotWidth = 5
        self.plotHeight = 4
        self.plotDPI = 100

        self.makeMenuBar()
        self.makeWidgets()
        self.addItems()
    
    def newFile(self):
        self.fileName = None
        self.shapes = []
        xfield = np.linspace(-self.mainwindow.xin, self.mainwindow.xin, self.mainwindow.N)
        yfield = np.linspace(-self.mainwindow.yin, self.mainwindow.yin, self.mainwindow.N)
        self.mask = Scalar_mask_XY(xfield, yfield, self.mainwindow.wavelength)

        self.drawMask(self.mask)

    def saveFile(self):
        if self.fileName == None:
            self.saveFileAs()
        else:

            file = open(self.fileName, "w")
            file.write(json.dumps(self.shapes))
            file.close()

    def openFile(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setNameFilter("*.json")
        fileDialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        fileDialog.setWindowTitle("Odpri masko")

        if fileDialog.exec_():
            self.fileName = fileDialog.selectedFiles()[0]
            file = open(self.fileName, "r")
            data = json.load(file)
            file.close()

            self.shapes = []
            xfield = np.linspace(-self.mainwindow.xin, self.mainwindow.xin, self.mainwindow.N)
            yfield = np.linspace(-self.mainwindow.yin, self.mainwindow.yin, self.mainwindow.N)
            self.mask = Scalar_mask_XY(xfield, yfield, self.mainwindow.wavelength)

            for obj in data:
                self.selected_mask_shape = obj["shape"]
                xfield = np.linspace(-self.mainwindow.xin, self.mainwindow.xin, self.mainwindow.N)
                yfield = np.linspace(-self.mainwindow.yin, self.mainwindow.yin, self.mainwindow.N)

                self.new_shape = Scalar_mask_XY(xfield, yfield, self.mainwindow.wavelength)

                
                if self.selected_mask_shape == "Trikotnik":
                    self.mask = self.addShapeToMask(self.mask, self.new_shape.triangle, obj["func_data"], obj["x_data"], obj["y_data"])
                elif self.selected_mask_shape == "Pravokotnik":
                    self.mask = self.addShapeToMask(self.mask, self.new_shape.square, obj["func_data"], obj["x_data"], obj["y_data"])
                elif self.selected_mask_shape == "Krog":
                    self.mask = self.addShapeToMask(self.mask, self.new_shape.circle, obj["func_data"], obj["x_data"], obj["y_data"])
                elif self.selected_mask_shape == "Poligon":
                    signature = self.mainwindow.get_default_args(self.new_shape.polygon)
                elif self.selected_mask_shape == "Navadni poligon":
                    signature = self.mainwindow.get_default_args(self.new_shape.regular_polygon)
                elif self.selected_mask_shape == "Zvezda":
                    self.mask = self.addShapeToMask(self.mask, self.new_shape.star, obj["func_data"], obj["x_data"], obj["y_data"])
                elif self.selected_mask_shape == "Obroči":
                    self.mask = self.addShapeToMask(self.mask, self.new_shape.rings, obj["func_data"], obj["x_data"], obj["y_data"])
                elif self.selected_mask_shape == "Križ":
                    self.mask = self.addShapeToMask(self.mask, self.new_shape.cross, obj["func_data"], obj["x_data"], obj["y_data"])
            
            self.drawMask(self.mask)
    
    def saveFileAs(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setNameFilter("*.json")
        fileDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fileDialog.setWindowTitle("Shrani masko kot ...")
        fileDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

        if fileDialog.exec_():
            self.fileName = fileDialog.selectedFiles()[0]
            if self.fileName.split(".")[-1].lower() != "json":
                self.fileName = self.fileName + ".json"
            
            self.saveFile()

    def makeMaskFromShapeList(self, shapes):
        xfield = np.linspace(-self.mainwindow.xin, self.mainwindow.xin, self.mainwindow.N)
        yfield = np.linspace(-self.mainwindow.yin, self.mainwindow.yin, self.mainwindow.N)
        self.mask = Scalar_mask_XY(xfield, yfield, self.mainwindow.wavelength)

        for obj in shapes:
            self.selected_mask_shape = obj["shape"]
            xfield = np.linspace(-self.mainwindow.xin, self.mainwindow.xin, self.mainwindow.N)
            yfield = np.linspace(-self.mainwindow.yin, self.mainwindow.yin, self.mainwindow.N)

            self.new_shape = Scalar_mask_XY(xfield, yfield, self.mainwindow.wavelength)
            
            if self.selected_mask_shape == "Trikotnik":
                self.mask = self.addShapeToMask(self.mask, self.new_shape.triangle, obj["func_data"], obj["x_data"], obj["y_data"])
            elif self.selected_mask_shape == "Pravokotnik":
                self.mask = self.addShapeToMask(self.mask, self.new_shape.square, obj["func_data"], obj["x_data"], obj["y_data"])
            elif self.selected_mask_shape == "Krog":
                self.mask = self.addShapeToMask(self.mask, self.new_shape.circle, obj["func_data"], obj["x_data"], obj["y_data"])
            elif self.selected_mask_shape == "Poligon":
                signature = self.mainwindow.get_default_args(self.new_shape.polygon)
            elif self.selected_mask_shape == "Navadni poligon":
                signature = self.mainwindow.get_default_args(self.new_shape.regular_polygon)
            elif self.selected_mask_shape == "Zvezda":
                self.mask = self.addShapeToMask(self.mask, self.new_shape.star, obj["func_data"], obj["x_data"], obj["y_data"])
            elif self.selected_mask_shape == "Obroči":
                self.mask = self.addShapeToMask(self.mask, self.new_shape.rings, obj["func_data"], obj["x_data"], obj["y_data"])
            elif self.selected_mask_shape == "Križ":
                self.mask = self.addShapeToMask(self.mask, self.new_shape.cross, obj["func_data"], obj["x_data"], obj["y_data"])
        
        return self.mask

    def makeWidgets(self):
        self.layout = QtWidgets.QHBoxLayout()

        self.componentsListWidget = QtWidgets.QListWidget()
        #self.componentsListWidget.setStyleSheet("background: gray")
        self.componentsListWidget.itemActivated.connect(self.addShape)
        self.layout.addWidget(self.componentsListWidget, 15)

        self.fig = Figure(figsize=(self.plotWidth, self.plotHeight), dpi=self.plotDPI)
        self.maskCanvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.maskCanvas, 70)

        self.ax = self.fig.add_subplot(111)

        self.dataWidget = QtWidgets.QWidget()
        self.dataWidget.setStyleSheet("background: white; border: 1px solid gray")
        self.layout.addWidget(self.dataWidget, 15)

        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)

    def makeMenuBar(self):
        self.menu = self.menuBar()

        self.fileMenu = self.menu.addMenu("&Datoteka")

        self.newFileButton = QtWidgets.QAction("&Nova maska")
        self.newFileButton.triggered.connect(self.newFile)
        self.newFileButton.setShortcut(QtGui.QKeySequence("Ctrl+n"))
        self.fileMenu.addAction(self.newFileButton)

        self.openFileButton = QtWidgets.QAction("&Odpri masko")
        self.openFileButton.triggered.connect(self.openFile)
        self.openFileButton.setShortcut(QtGui.QKeySequence("Ctrl+o"))
        self.fileMenu.addAction(self.openFileButton)

        self.fileMenu.addSeparator()

        self.saveFileButton = QtWidgets.QAction("&Shrani masko")
        self.saveFileButton.triggered.connect(self.saveFile)
        self.saveFileButton.setShortcut(QtGui.QKeySequence("Ctrl+s"))
        self.fileMenu.addAction(self.saveFileButton)

        self.saveFileAsButton = QtWidgets.QAction("Shrani masko &kot")
        self.saveFileAsButton.triggered.connect(self.saveFileAs)
        self.saveFileAsButton.setShortcut(QtGui.QKeySequence("Ctrl+Shift+s"))
        self.fileMenu.addAction(self.saveFileAsButton)

    def addItems(self):
        self.componentsListWidget.addItem("Trikotnik")
        self.componentsListWidget.addItem("Pravokotnik")
        self.componentsListWidget.addItem("Krog")
        self.componentsListWidget.addItem("Poligon")
        self.componentsListWidget.addItem("Navadni poligon")
        self.componentsListWidget.addItem("Zvezda")
        self.componentsListWidget.addItem("Obroči")
        self.componentsListWidget.addItem("Križ")

    def addShape(self, item):
        self.selected_mask_shape = item.text()
        self.addItemLayout = QtWidgets.QVBoxLayout()

        signature = None

        xfield = np.linspace(-self.mainwindow.xin, self.mainwindow.xin, self.mainwindow.N)
        yfield = np.linspace(-self.mainwindow.yin, self.mainwindow.yin, self.mainwindow.N)

        self.new_shape = Scalar_mask_XY(xfield, yfield, self.mainwindow.wavelength)

        label = QtWidgets.QLabel(self.selected_mask_shape)
        label.setStyleSheet("border: none")
        self.addItemLayout.addWidget(label)

        if self.selected_mask_shape == "Trikotnik":
            signature = self.mainwindow.get_default_args(self.new_shape.triangle)
        elif self.selected_mask_shape == "Pravokotnik":
            signature = self.mainwindow.get_default_args(self.new_shape.square)
        elif self.selected_mask_shape == "Krog":
            signature = self.mainwindow.get_default_args(self.new_shape.circle)
        elif self.selected_mask_shape == "Poligon":
            return
            #signature = self.mainwindow.get_default_args(self.new_shape.polygon)
        elif self.selected_mask_shape == "Navadni poligon":
            return
            #signature = self.mainwindow.get_default_args(self.new_shape.regular_polygon)
        elif self.selected_mask_shape == "Zvezda":
            return
            #signature = self.mainwindow.get_default_args(self.new_shape.star)
        elif self.selected_mask_shape == "Obroči":
            return
            #signature = self.mainwindow.get_default_args(self.new_shape.rings)
        elif self.selected_mask_shape == "Križ":
            signature = self.mainwindow.get_default_args(self.new_shape.cross)

        for arg in signature:
            initial_val = signature[arg]

            if type(initial_val) != int and type(initial_val) != float:
                label = QtWidgets.QLabel(arg)
                label.setStyleSheet("border: none")
                x_edit = LineEditWithLabel("X:", 0)
                y_edit = LineEditWithLabel("Y:", 0)

                vlayout = QtWidgets.QVBoxLayout()
                hlayout = QtWidgets.QHBoxLayout()
                hlayout.addWidget(x_edit)
                hlayout.addWidget(y_edit)
                vlayout.addWidget(label)
                vlayout.addLayout(hlayout)
                self.addItemLayout.addLayout(vlayout)
            else:
                line_edit = LineEditWithLabel(arg, initial_val)
                self.addItemLayout.addWidget(line_edit)

        x_num = LineEditWithLabel("Število ponovitev x:", 1)
        y_num = LineEditWithLabel("Število ponovitev y:", 1)

        x_diff = LineEditWithLabel("Razmak x:", 50)
        y_diff = LineEditWithLabel("Razmak y:", 50)

        xLayout = QtWidgets.QHBoxLayout()
        xLayout.addWidget(x_num)
        xLayout.addWidget(x_diff)

        yLayout = QtWidgets.QHBoxLayout()
        yLayout.addWidget(y_num)
        yLayout.addWidget(y_diff)

        self.addItemLayout.addLayout(xLayout)
        self.addItemLayout.addLayout(yLayout)

        buttonLayout = QtWidgets.QHBoxLayout()
        preshowBtn = QtWidgets.QPushButton("Prikaži")
        preshowBtn.clicked.connect(self.preshowMask)
        
        submitBtn = QtWidgets.QPushButton("Dodaj")
        submitBtn.clicked.connect(self.applyShape)

        buttonLayout.addWidget(preshowBtn)
        buttonLayout.addWidget(submitBtn)
        self.addItemLayout.addLayout(buttonLayout)

        if self.dataWidget.layout() != None:
            QtWidgets.QWidget().setLayout(self.dataWidget.layout())
        self.dataWidget.setLayout(self.addItemLayout)

    def showEvent(self, event):
        self.drawMask(self.mask)
        event.accept()

    def getDataLayout(self, layout, tab = ""):
        data = []

        for i in range(layout.count()):
            item = layout.itemAt(i)
            #print(tab, i, type(item), item)

            if type(item) == QtWidgets.QVBoxLayout or type(item) == QtWidgets.QHBoxLayout:
                subData = self.getDataLayout(item.layout(), tab + "\t")
                if len(subData) == 1:
                    data.append(subData[0])
                else:
                    data.append(subData)
            else:
                widget = item.widget()
                if isinstance(widget, LineEditWithLabel):
                    data.append(float(widget.line_edit.text()))
            
        return data
    
    def addShapeToMask(self, mask, func, func_data, x_data, y_data):
        for y in range(int(y_data[0])):
            for x in range(int(x_data[0])):
                func([func_data[0][0] + x * x_data[1], func_data[0][1] + y * y_data[1]], *func_data[1:])
                mask = mask.add(self.new_shape)

        return mask

    def preshowMask(self):
        data = self.getDataLayout(self.addItemLayout)

        xfield = np.linspace(-self.mainwindow.xin, self.mainwindow.xin, self.mainwindow.N)
        yfield = np.linspace(-self.mainwindow.yin, self.mainwindow.yin, self.mainwindow.N)

        premask = Scalar_mask_XY(xfield, yfield, self.mainwindow.wavelength)
        premask.u = np.copy(self.mask.u)

        func_data, x_data, y_data = data[:-3], data[-3], data[-2]
        #print(func_data, x_data, y_data)

        if self.selected_mask_shape == "Trikotnik":
            premask = self.addShapeToMask(premask, self.new_shape.triangle, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Pravokotnik":
            premask = self.addShapeToMask(premask, self.new_shape.square, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Krog":
            premask = self.addShapeToMask(premask, self.new_shape.circle, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Poligon":
            signature = self.mainwindow.get_default_args(self.new_shape.polygon)
        elif self.selected_mask_shape == "Navadni poligon":
            signature = self.mainwindow.get_default_args(self.new_shape.regular_polygon)
        elif self.selected_mask_shape == "Zvezda":
            premask = self.addShapeToMask(premask, self.new_shape.star, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Obroči":
            premask = self.addShapeToMask(premask, self.new_shape.rings, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Križ":
            premask = self.addShapeToMask(premask, self.new_shape.cross, func_data, x_data, y_data)

        self.drawMask(premask)

    def applyShape(self, data = None):
        data = self.getDataLayout(self.addItemLayout)

        func_data, x_data, y_data = data[:-3], data[-3], data[-2]

        self.shapes.append({"shape": self.selected_mask_shape, "func_data": func_data, "x_data": x_data, "y_data": y_data})

        if self.selected_mask_shape == "Trikotnik":
            self.mask = self.addShapeToMask(self.mask, self.new_shape.triangle, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Pravokotnik":
            self.mask = self.addShapeToMask(self.mask, self.new_shape.square, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Krog":
            self.mask = self.addShapeToMask(self.mask, self.new_shape.circle, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Poligon":
            signature = self.mainwindow.get_default_args(self.new_shape.polygon)
        elif self.selected_mask_shape == "Navadni poligon":
            signature = self.mainwindow.get_default_args(self.new_shape.regular_polygon)
        elif self.selected_mask_shape == "Zvezda":
            self.mask = self.addShapeToMask(self.mask, self.new_shape.star, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Obroči":
            self.mask = self.addShapeToMask(self.mask, self.new_shape.rings, func_data, x_data, y_data)
        elif self.selected_mask_shape == "Križ":
            self.mask = self.addShapeToMask(self.mask, self.new_shape.cross, func_data, x_data, y_data)

        if self.dataWidget.layout() != None:
            QtWidgets.QWidget().setLayout(self.dataWidget.layout())

        self.drawMask(self.mask)

    def drawMask(self, mask):
        maskTuple = mask.draw()
        #plt.show()
        #print(maskTuple)
        subplot, axes_image = maskTuple[1], maskTuple[2]

        xlim = subplot.get_xlim()
        ylim = subplot.get_ylim()

        self.ax.clear()
        self.ax.imshow(axes_image.get_array(), cmap="gray", extent=[xlim[0], xlim[1], ylim[0], ylim[1]], origin="lower")
        self.ax.set_xlabel(subplot.get_xlabel())
        self.ax.set_ylabel(subplot.get_ylabel())
        
        self.maskCanvas.draw()

    def passMaskToMainProgram(self):
        self.mainwindow.setOpticalElementProperties()

    def closeEvent(self, event):
        if self.mainwindow and len(self.shapes) > 0:
            self.passMaskToMainProgram()