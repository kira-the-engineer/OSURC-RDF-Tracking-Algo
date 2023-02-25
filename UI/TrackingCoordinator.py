from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
#get path to tracking algorithm
sys.path.insert(1, '/home/groundstation/github/OSURC-RDF-Tracking-Algo/rover_gps')
import tracking_algorithm

class TrackingCore(QtWidgets.QWidget):
    def __init__(self):
        super(TrackingCore, self).__init__()
        trackingAlgo = tracking_algorithm.TrackingAlgorithm()
        uic.loadUi('TrackingAlgoDisp.ui', self)
        self.show()

	self.rover_lat = QLabel()
	self.rover_lon = QLabel()

    def on_update_rover_coordinates_ready(self, algo):
        

app = QtWidgets.QApplication(sys.argv)
window = TrackingCore()
app.exec_()
