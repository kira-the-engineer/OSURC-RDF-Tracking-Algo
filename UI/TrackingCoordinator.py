from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
#import tracking_algorithm

class TrackingCore(QtWidgets.QWidget):
    def __init__(self):
        super(TrackingCore, self).__init__()
        uic.loadUi('TrackingAlgoDisp.ui', self)
        self.show()

app = QtWidgets.QApplication(sys.argv)
window = TrackingCore()
app.exec_()
