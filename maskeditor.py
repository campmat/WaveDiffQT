from PyQt5 import QtCore, QtGui, QtWidgets

import math

class MaskEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mask Editor")
        self.resize(1600, 1000)

        self.makeMenuBar()
        self.makeWidgets()
    
    def newFile(self):
        pass

    def saveFile(self):
        pass

    def openFile(self):
        pass
    
    def saveFileAs(self):
        pass

    def makeWidgets(self):
        self.layout = QtWidgets.QHBoxLayout()

        self.componentsListWidget = QtWidgets.QWidget()
        self.componentsListWidget.setStyleSheet("background: gray")
        self.layout.addWidget(self.componentsListWidget, 15)

        schemeLayout = QtWidgets.QVBoxLayout()

        self.schemeWidget = QtWidgets.QWidget()
        self.schemeWidget.setStyleSheet("background: black")
        schemeLayout.addWidget(self.schemeWidget)
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

    def createPoly(self, n, r, s, xOff, yOff):
        polygon = QtGui.QPolygonF() 
        w = 360/n
        for i in range(n):
            t = w*i + s
            x = r*math.cos(math.radians(t))
            y = r*math.sin(math.radians(t))
            polygon.append(QtCore.QPointF(x + xOff, y + yOff))  

        return polygon

    def paintEvent(self, event):
        self.pen = QtGui.QPen(QtGui.QColor(255,255,255))
        self.pen.setWidth(2)
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))

        triangle = self.createPoly(3, 50, 0, self.componentsListWidget.width() / 2, 10)
        square = self.createPoly(4, 50, 0, self.componentsListWidget.width() / 2, 60)

        painter = QtGui.QPainter(self.componentsListWidget)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        painter.drawPolygon(triangle)
        painter.drawPolygon(square)


    def dragEnterEvent(self, e):
        e.accept()
        print(e)

    def dropEvent(self, e):
        print(e)