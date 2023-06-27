import sys
from PyQt5 import QtWidgets, uic
from mainwindow import MainWindow

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()