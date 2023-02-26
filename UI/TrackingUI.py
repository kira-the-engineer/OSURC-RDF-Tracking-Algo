from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys

class TrackingUI(QtWidgets.QWidget):
    def __init__(self):
        super(TrackingUI, self).__init__()
        uic.loadUi('TrackingAlgoDisp.ui', self)
        self.show()

app = QtWidgets.QApplication(sys.argv)
window = TrackingUI()
app.exec_()
