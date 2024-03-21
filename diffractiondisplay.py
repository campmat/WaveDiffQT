from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np

from diffractio.scalar_masks_XY import Scalar_mask_XY

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class FloatSlider(QtWidgets.QSlider):
    def __init__(self, orientation=QtCore.Qt.Horizontal, *args, decimals=2, **kwargs):
        super().__init__(orientation, *args, **kwargs)
        self._multiplier = 10 ** decimals
        self._decimals = decimals

    def setFloatValue(self, value):
        int_value = int(value * self._multiplier)
        self.setValue(int_value)

    def floatValue(self):
        return self.value() / self._multiplier

class DiffractionDisplay(QtWidgets.QMainWindow):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        self.setWindowTitle("Diffraction Display")
        self.resize(1600, 1000)

        self.plotWidth = 5
        self.plotHeight = 4
        self.plotDPI = 100

        self.kindOptions = ["amplitude", "intensity", "field", "phase", "fill", "fft"]
        self.kindIndex = 1

        self.logarithm = False
        self.normalize = False

        self.cut_value = None

        self.fileName = ""

        self.scaleOptions = ["", "scaled", "equal"]
        self.scaleIndex = 0

        self.u = None

        self.makeMenuBar()
        self.makeWidgets()

    def savePicture(self):
        if self.u != None:
            self.u.draw(kind=self.kindOptions[self.kindIndex], logarithm=self.logarithm, normalize=self.normalize, cut_value=self.cut_value, scale=self.scaleOptions[self.scaleIndex])

    def makeMenuBar(self):
        self.menu = self.menuBar()

        self.fileMenu = self.menu.addMenu("&Datoteka")

        self.saveFileButton = QtWidgets.QAction("&Shrani sliko")
        self.saveFileButton.triggered.connect(self.savePicture)
        self.saveFileButton.setShortcut(QtGui.QKeySequence("Ctrl+s"))
        self.fileMenu.addAction(self.saveFileButton)

    def makeWidgets(self):
        self.layout = QtWidgets.QHBoxLayout()

        self.fig = Figure(figsize=(self.plotWidth, self.plotHeight), dpi=self.plotDPI)
        self.maskCanvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.maskCanvas, 80)

        self.ax = self.fig.add_subplot(111)

        self.settingsWidget = QtWidgets.QWidget()
        self.settingsWidget.setStyleSheet("background: gray; border: 1px solid gray")
        settingsLayout = QtWidgets.QVBoxLayout()

        kindHLayout = QtWidgets.QHBoxLayout()
        self.kindLabel = QtWidgets.QLabel("Kind:")
        self.kindComboBox = QtWidgets.QComboBox()
        self.kindComboBox.addItems(self.kindOptions)
        self.kindComboBox.setCurrentIndex(self.kindIndex)
        self.kindComboBox.currentIndexChanged.connect(self.kindChanged)
        kindHLayout.addWidget(self.kindLabel)
        kindHLayout.addWidget(self.kindComboBox)
        settingsLayout.addLayout(kindHLayout)

        logarithmHLayout = QtWidgets.QHBoxLayout()
        self.logarithmLabel = QtWidgets.QLabel("Logarithm:")
        self.logarithmCheckBox = QtWidgets.QCheckBox()
        self.logarithmCheckBox.setChecked(self.logarithm)
        self.logarithmCheckBox.stateChanged.connect(self.logarithmChanged)
        logarithmHLayout.addWidget(self.logarithmLabel)
        logarithmHLayout.addWidget(self.logarithmCheckBox)
        settingsLayout.addLayout(logarithmHLayout)

        normalizeHLayout = QtWidgets.QHBoxLayout()
        self.normalizeLabel = QtWidgets.QLabel("Normalize:")
        self.normalizeCheckBox = QtWidgets.QCheckBox()
        self.normalizeCheckBox.setChecked(self.normalize)
        self.normalizeCheckBox.stateChanged.connect(self.normalizeChanged)
        normalizeHLayout.addWidget(self.normalizeLabel)
        normalizeHLayout.addWidget(self.normalizeCheckBox)
        settingsLayout.addLayout(normalizeHLayout)

        cutValueHLayout = QtWidgets.QHBoxLayout()
        self.cutValueLabel = QtWidgets.QLabel("Cut value:")
        self.cutValueSlider = FloatSlider()
        self.cutValueSlider.valueChanged.connect(self.cutValueSliderChanged)
        self.cutValueLineEdit = QtWidgets.QLineEdit()
        self.cutValueLineEdit.setText("0")
        self.cutValueLineEdit.textChanged.connect(self.cutValueChanged)

        cutValueHLayout.addWidget(self.cutValueLabel)
        cutValueHLayout.addWidget(self.cutValueSlider)
        cutValueHLayout.addWidget(self.cutValueLineEdit)
        settingsLayout.addLayout(cutValueHLayout)

        scaleHLayout = QtWidgets.QHBoxLayout()
        self.scaleLabel = QtWidgets.QLabel("Kind:")
        self.scaleComboBox = QtWidgets.QComboBox()
        self.scaleComboBox.addItems(self.scaleOptions)
        self.scaleComboBox.setCurrentIndex(self.scaleIndex)
        self.scaleComboBox.currentIndexChanged.connect(self.scaleChanged)
        scaleHLayout.addWidget(self.scaleLabel)
        scaleHLayout.addWidget(self.scaleComboBox)
        settingsLayout.addLayout(scaleHLayout)
        
        self.settingsWidget.setLayout(settingsLayout)
        self.layout.addWidget(self.settingsWidget, 20)

        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.layout)
        self.setCentralWidget(self.mainWidget)

    def kindChanged(self, index):
        self.kindIndex = index
        self.showScalarField(self.u)

    def logarithmChanged(self, state):
        self.logarithm = state == QtCore.Qt.Checked
        self.showScalarField(self.u)

    def normalizeChanged(self, state):
        self.normalize = state == QtCore.Qt.Checked
        self.showScalarField(self.u)

    def cutValueSliderChanged(self):
        value = self.cutValueSlider.floatValue()
        if value <= 0:
            value = None
        elif value >= 1:
            value = 1
            self.cutValueSlider.setFloatValue(1)
        
        self.cutValueLineEdit.setText(str(value))
        self.cut_value = value
        self.showScalarField(self.u)

    def cutValueChanged(self, text):
        if text == "" or text == "None" or float(text) <= 0:
            self.cut_value = None
    
        if float(text) > 1:
            text = "1"
        
        self.cut_value = float(text)
        self.cutValueSlider.setFloatValue(float(text))

        self.showScalarField(self.u)

    def scaleChanged(self, index):
        self.scaleIndex = index
        self.showScalarField(self.u)

    def showScalarField(self, u):
        if u == None:
            return
        
        self.u = u
        maskTuple = u.draw(kind=self.kindOptions[self.kindIndex], logarithm=self.logarithm, normalize=self.normalize, cut_value=self.cut_value, scale=self.scaleOptions[self.scaleIndex])

        subplot, axes_image = maskTuple[1], maskTuple[2]

        xlim = subplot.get_xlim()
        ylim = subplot.get_ylim()

        self.ax.clear()
        self.ax.imshow(axes_image.get_array(), cmap="gray", extent=[xlim[0], xlim[1], ylim[0], ylim[1]], origin="lower")
        self.ax.set_xlabel(subplot.get_xlabel())
        self.ax.set_ylabel(subplot.get_ylabel())

        self.maskCanvas.draw()