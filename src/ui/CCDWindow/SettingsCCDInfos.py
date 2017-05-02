from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QPushButton, QVBoxLayout, QWidget)

from src.ui.commons.layout import set_lvbox, set_hbox
from src.utils.camera.SbigDriver import (ccdinfo, getlinkstatus)


class SettingsCCDInfos(QWidget):
    def __init__(self, parent=None):
        super(SettingsCCDInfos, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.createFilterWheelGroup(), 0, 0)
        grid.addWidget(self.createCCDCameraGroup(), 1, 0)
        grid.addWidget(self.createPushButtonGroup(), 2, 0)
        self.setLayout(grid)

        self.setWindowTitle("Imager Box")
        self.resize(500, 340)

    def createFilterWheelGroup(self):
        groupBox = QGroupBox("INFOS")

        radio1 = QtWidgets.QLabel("Camera Port COM1", self)
        radio1.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        radio2 = QtWidgets.QLabel("Camera model: 6", self)
        radio2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        radio3 = QtWidgets.QLabel("Pixel array:  TESTETE", self)
        radio3.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createCCDCameraGroup(self):
        groupBox = QGroupBox("Settings")
        groupBox.setCheckable(True)
        groupBox.setChecked(False)

        self.shutter_l = QtWidgets.QLabel("Shutter:", self)
        self.shutter_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.close_open = QtWidgets.QComboBox(self)
        self.close_open.setMaximumWidth(100)
        self.fill_combo_close_open()

        self.temp_setpoint_l = QtWidgets.QLabel("CCD Temp Set Point:", self)
        self.temp_setpoint_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.temp_setpoint_f = QtWidgets.QLineEdit(self)
        self.temp_setpoint_f.setMaximumWidth(100)

        self.temp_init_l = QtWidgets.QLabel("Tempo para iniciar:", self)
        self.temp_init_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.temp_init_f = QtWidgets.QLineEdit(self)
        self.temp_init_f.setMaximumWidth(100)

        self.btn_one_photo = QtWidgets.QPushButton('Take Photo', self)

        self.tempButton = QtWidgets.QPushButton("Set Temp", self)

        self.fanButton = QtWidgets.QPushButton("Fan (On/Off)")

        groupBox.setLayout(set_lvbox(set_hbox(self.shutter_l, self.close_open),
                                     set_hbox(self.temp_setpoint_l, self.temp_setpoint_f),
                                     set_hbox(self.temp_init_l, self.temp_init_f),
                                     set_hbox(self.btn_one_photo, self.tempButton, self.fanButton, stretch2=1)))
        return groupBox

    def createPushButtonGroup(self):
        groupBox = QGroupBox("&Push Buttons")
        groupBox.setCheckable(True)
        groupBox.setChecked(True)

        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        self.clearButton = QPushButton("Clear")

        groupBox.setLayout(set_lvbox(set_hbox(self.saveButton, self.clearButton, self.cancelButton)))

        return groupBox

    def get_info_pixels(self):
        '''
        Function to get the CCD Info
        This function will return [Pixels]
        '''
        ret = None
        self.lock.set_acquire()
        try:
            ret = tuple(ccdinfo())
        except Exception as e:
            self.console.raise_text("Failed to get camera information.\n{}".format(e))
        finally:
            self.lock.set_release()
        return ret

    def fill_combo_close_open(self):
        self.close_open.addItem("Open", 0)
        self.close_open.addItem("Close", 1)

    def teste(self):
        pass
