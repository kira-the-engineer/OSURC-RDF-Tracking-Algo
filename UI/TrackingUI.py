from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import TrackingCoordinator as track
from functools import partial

class TrackingUI(QtWidgets.QWidget):
	def __init__(self):
		super(TrackingUI, self).__init__()
		uic.loadUi('TrackingAlgoDisp.ui', self)
		self.tThread = track.TrackingCore()
		self.tThread.rover_lat_update_ready__signal.connect(self.updateRLat)
		self.tThread.rover_lon_update_ready__signal.connect(self.updateRLon)
		self.tThread.base_lat_update_ready__signal.connect(self.updateBLat)
		self.tThread.base_lon_update_ready__signal.connect(self.updateBLon)
		self.tThread.start()
		
		#only enable PB for manual angle on valid input in text box, default state is disabled
		self.manual_angle_pb.setEnabled(False)
		#set validator for angle text
		validator = QtGui.QDoubleValidator(0.00, 360.00, 2)
		self.manual_angle_text.setValidator(validator)
	
	def updateRLat(self, value):
		self.rover_lat.setNum(value)
    	
	def updateRLon(self, value):
		self.rover_lon.setNum(value)
		
	def updateBLat(self, value):
		self.base_lat.setNum(value)
		
	def updateBLon(self, value):
		self.base_lon.setNum(value)
		
	#trigger this on keyboard input instead of lineEdit finished, because validator prevents editingFinished and returnPressed updates with invalid numbers
	def verify_angle(self, validator):
		state = validator.validate(self.manual_angle_text.text(), 0)
		print(state[0])
		
		"""
		if(state[0] == QtGui.QValidator.Acceptable):
			self.manual_angle_pb.setEnabled(True)
		if(state[0] == QtGui.QValidator.Invalid || state[0] == QtGui.QValidator.Intermediate)
			self.manual_angle_pb.setEnabled(False)
		"""
		 

app = QtWidgets.QApplication(sys.argv)
window = TrackingUI()
window.show()
app.exec_()
