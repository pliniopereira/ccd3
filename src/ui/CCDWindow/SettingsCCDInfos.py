from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QPushButton, QWidget)

from src.controller.camera import Camera
from src.ui.commons.layout import set_hbox, set_lvbox
from src.utils.camera.SbigDriver import (ccdinfo)
from src.utils.rodafiltros.FilterControl import *


class SettingsCCDInfos(QWidget):
    def __init__(self, parent=None):
        super(SettingsCCDInfos, self).__init__(parent)

        self.cam = Camera()
        self.roda_filtros = FilterControl()

        try:
            self.firmware, self.model, self.y_pixels, self.x_pixels =\
                self.cam.get_firmware_and_model_and_pixels()
        except Exception as e:
            print(e)
            self.firmware, self.model, self.y_pixels, self.x_pixels = "????", "????",\
                                                                      "????", "????"

        grid = QGridLayout()
        grid.addWidget(self.createFilterWheelInfoGroup(), 0, 0)
        grid.addWidget(self.createFilterWheelGroup(), 1, 0)
        grid.addWidget(self.createCCDInfoGroup(), 0, 1)
        grid.addWidget(self.createCCDCameraGroup(), 1, 1)
        grid.addWidget(self.createPushButtonGroup(), 2, 1)
        self.setLayout(grid)

        self.button_settings()

        self.setWindowTitle("Imager Box")
        self.resize(500, 340)

    def createFilterWheelInfoGroup(self):
        groupBox = QGroupBox("&Filter Wheel Info")

        self.serial_filter_wheel_info_l = QtWidgets.QLabel("Serial Port: ", self)
        self.serial_filter_wheel_info_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        try:
            motor_door_aux = str(self.roda_filtros.motor_door)
        except Exception as e:
            print(e)
            motor_door_aux = "???"

        self.serial_filter_wheel_info_f = QtWidgets.QLabel(motor_door_aux, self)
        self.serial_filter_wheel_info_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.slots_filter_wheel_info_l = QtWidgets.QLabel("Filter Slot: ", self)
        self.slots_filter_wheel_info_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.slots_filter_wheel_info_f = QtWidgets.QLabel("6", self)
        self.slots_filter_wheel_info_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.tempt_filter_wheel_info_l = QtWidgets.QLabel("Filter Temperature: ", self)
        self.tempt_filter_wheel_info_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tempt_filter_wheel_info_f = QtWidgets.QLabel("25 °C", self)
        self.tempt_filter_wheel_info_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        groupBox.setLayout(set_lvbox(set_hbox(self.serial_filter_wheel_info_l, self.serial_filter_wheel_info_f),
                                     set_hbox(self.slots_filter_wheel_info_l, self.slots_filter_wheel_info_f),
                                     set_hbox(self.tempt_filter_wheel_info_l, self.tempt_filter_wheel_info_f)))

        return groupBox

    def createFilterWheelGroup(self):
        groupBox = QGroupBox("&Filter Weel Control")
        groupBox.setCheckable(True)
        groupBox.setChecked(False)

        self.shutter_l = QtWidgets.QLabel("Shutter:", self)
        self.shutter_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.close_open_filter_wheel = QtWidgets.QComboBox(self)
        self.close_open_filter_wheel.setMaximumWidth(100)
        self.fill_combo_close_open_filter_wheel_shutter()

        self.btn_get_filter = QtWidgets.QPushButton('Get filter', self)
        self.filter_position = QtWidgets.QLabel(self.roda_filtros.get_filtro_atual())
        self.filter_position.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.filter_position.setMinimumWidth(60)

        self.btn_set_filter = QtWidgets.QPushButton('Set filter', self)
        self.set_filter_position = QtWidgets.QComboBox(self)
        self.set_filter_position.setMaximumWidth(100)
        self.fill_combo_filter_position()

        self.btn_home_position_filter = QtWidgets.QPushButton('Home Reset', self)

        groupBox.setLayout(set_lvbox(set_hbox(self.shutter_l, self.close_open_filter_wheel),
                                     set_hbox(self.btn_get_filter, self.filter_position, stretch2=1),
                                     set_hbox(self.btn_set_filter, self.set_filter_position),
                                     set_hbox(self.btn_home_position_filter)))
        return groupBox

    def createCCDInfoGroup(self):
        groupBox = QGroupBox("Info CCD")

        self.info_port_ccd_l = QtWidgets.QLabel("Camera Firmware: ", self)
        self.info_port_ccd_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.info_port_ccd_f = QtWidgets.QLabel(self.firmware)
        self.info_port_ccd_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.info_camera_model_l = QtWidgets.QLabel("Camera Model: ", self)
        self.info_camera_model_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.info_camera_model_f = QtWidgets.QLabel(self.model)
        self.info_camera_model_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.info_pixel_array_l = QtWidgets.QLabel("Pixel array: ", self)
        self.info_pixel_array_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.info_pixel_array_f = QtWidgets.QLabel(self.x_pixels + " X " + self.y_pixels + " Pixels")
        self.info_pixel_array_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        groupBox.setLayout(set_lvbox(set_hbox(self.info_port_ccd_l, self.info_port_ccd_f),
                                     set_hbox(self.info_camera_model_l, self.info_camera_model_f),
                                     set_hbox(self.info_pixel_array_l, self.info_pixel_array_f)))
        return groupBox

    def createCCDCameraGroup(self):
        groupBox = QGroupBox("Settings")
        groupBox.setCheckable(True)
        groupBox.setChecked(False)

        self.shutter_l = QtWidgets.QLabel("Shutter:", self)
        self.shutter_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.close_open = QtWidgets.QComboBox(self)
        self.close_open.setMaximumWidth(100)
        self.fill_combo_close_open_ccd_shutter()

        self.temp_setpoint_l = QtWidgets.QLabel("CCD Temp Set Point (°C):", self)
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
        #groupBox.setCheckable(True)
        #groupBox.setChecked(True)

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

    def fill_combo_close_open_ccd_shutter(self):
        self.close_open.addItem("Open", 0)
        self.close_open.addItem("Close", 1)

    def fill_combo_close_open_filter_wheel_shutter(self):
        self.close_open_filter_wheel.addItem("Open", 0)
        self.close_open_filter_wheel.addItem("Close", 1)

    def fill_combo_filter_position(self):
            self.set_filter_position.addItem("1", 1)
            self.set_filter_position.addItem("2", 2)
            self.set_filter_position.addItem("3", 3)
            self.set_filter_position.addItem("4", 4)
            self.set_filter_position.addItem("5", 5)
            self.set_filter_position.addItem("6", 6)

    def button_settings(self):
        self.btn_get_filter.clicked.connect(self.func_get_filter)
        self.btn_set_filter.clicked.connect(self.func_filter_position)
        self.btn_home_position_filter.clicked.connect(self.func_home_position)

    def func_get_filter(self):
        try:
            sleep(2)
            filter_position_aux = self.roda_filtros.get_filtro_atual()
            self.filter_position.setText(filter_position_aux)
            sleep(3)

        except Exception as e:
            print(e)

    def func_filter_position(self):
        try:
            sleep(1)
            self.roda_filtros.FilterWheel_Control(self.set_filter_position.currentIndex() + 1)
            sleep(1)

        except Exception as e:
            print(e)

    def func_home_position(self):
        try:
            sleep(1)
            print("func_home_position")
            self.roda_filtros.home_reset()
            sleep(1)

        except Exception as e:
            print(e)
