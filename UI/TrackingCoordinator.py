from PyQt5 import QtWidgets, QtCore, QtGui
import sys
#get path to tracking algorithm
sys.path.insert(1, '/home/groundstation/github/OSURC-RDF-Tracking-Algo/rover_gps')
import tracking_algorithm

#create threaded class to avoid blocking UI updates
class TrackingCore(QtCore.QThread):
	#create signals
	rover_lat_update_ready__signal = QtCore.pyqtSignal(float)
	rover_lon_update_ready__signal = QtCore.pyqtSignal(float)

	def __init__(self):
		super(TrackingCore,self).__init__()
		self.rover_lat = QLabel()
		self.rover_lon = QLabel()

		## Class Variables ##
		self.current_rover_lat = -1
		self.current_rover_lon = -1

	def rover_latitude_changed__slot(self, trackingAlgo):
		self.current_rover_lat = trackingAlgo.r_lat
		self.rover_lat_update_ready__signal.emit(current_rover_lat)

	def rover_longitide_changed__slot(self, trackingAlgo):
		self.current_rover_lon = trackingAlgo.r_lon
		self.rover_lon_update_ready__signal.emit(current_rover_lon)
