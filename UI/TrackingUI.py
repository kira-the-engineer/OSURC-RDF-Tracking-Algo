from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import TrackingCoordinator as track

class TrackingUI(QtWidgets.QWidget):
    def __init__(self):
        super(TrackingUI, self).__init__()
        uic.loadUi('TrackingAlgoDisp.ui', self)
        self.tThread = track.TrackingCore()
        self.tThread.rover_lat_update_ready__signal.connect(self.updateRLat)
        self.tThread.start()
	
    def updateRLat(self, value):
    	self.rover_lat.setNum(value)

app = QtWidgets.QApplication(sys.argv)
window = TrackingUI()
window.show()
app.exec_()
