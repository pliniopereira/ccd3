from time import sleep

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QPushButton, QWidget)

from src.business.configuration.settingsCamera import SettingsCamera
from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.controller.camera import Camera
from src.ui.commons.layout import set_hbox, set_lvbox
from src.utils.camera.SbigDriver import (ccdinfo)
from src.utils.rodafiltros.FilterControl import FilterControl


class SettingsCCDInfos(QWidget):
    def __init__(self, parent=None):
        super(SettingsCCDInfos, self).__init__(parent)

        self.imager_window = parent

        self.cam = Camera()

        self.roda_filtros = FilterControl()

        self.var_save_ini_camera = SettingsCamera()

        self.console = ConsoleThreadOutput()

        # Instance attributes create_filter_wheel_info_group
        self.serial_filter_wheel_info_l = None
        self.serial_filter_wheel_info_f = None
        self.tempt_filter_wheel_info_l = None
        self.tempt_filter_wheel_info_f = None
        self.slots_filter_wheel_info_l = None
        self.slots_filter_wheel_info_f = None

        # Instance attributes create_filter_wheel_group
        self.shutter_l = None
        self.close_open_filter_wheel = None
        self.get_filter_l = None
        self.filter_position = None
        self.btn_set_filter = None
        self.set_filter_position = None
        self.btn_home_position_filter = None

        # Instance attributes create_ccd_info_group
        self.info_port_ccd_l = None
        self.info_port_ccd_f = None
        self.info_camera_model_l = None
        self.info_camera_model_f = None
        self.info_pixel_array_l = None
        self.info_pixel_array_f = None

        # Instance attributes create_ccd_camera_group
        self.close_open = None
        self.temp_set_point_l = None
        self.temp_set_point_f = None
        self.temp_init_l = None
        self.temp_init_f = None
        self.btn_one_photo = None
        self.tempButton = None
        self.fanButton = None

        # Instance attributes create_push_button_group
        self.saveButton = None
        self.cancelButton = None
        self.clearButton = None

        try:
            self.firmware, self.model, self.y_pixels, self.x_pixels =\
                self.cam.get_firmware_and_model_and_pixels()
        except Exception as e:
            print(e)
            self.firmware, self.model, self.y_pixels, self.x_pixels = "????", "????", \
                                                                      "????", "????"

        grid = QGridLayout()
        grid.addWidget(self.create_filter_wheel_info_group(), 0, 0)
        grid.addWidget(self.create_filter_wheel_group(), 1, 0)
        grid.addWidget(self.create_ccd_info_group(), 0, 1)
        grid.addWidget(self.create_ccd_camera_group(), 1, 1)
        grid.addWidget(self.create_push_button_group(), 2, 1)
        self.setLayout(grid)

        self.button_settings()

        self.setWindowTitle("Imager Box")
        self.resize(500, 340)

    def create_filter_wheel_info_group(self):
        group_box = QGroupBox("&Filter Wheel Info")

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

        group_box.setLayout(set_lvbox(set_hbox(self.serial_filter_wheel_info_l, self.serial_filter_wheel_info_f), 
                                      set_hbox(self.slots_filter_wheel_info_l, self.slots_filter_wheel_info_f), 
                                      set_hbox(self.tempt_filter_wheel_info_l, self.tempt_filter_wheel_info_f)))

        return group_box

    def create_filter_wheel_group(self):
        group_box = QGroupBox("&Filter Wheel Control")
        group_box.setCheckable(True)
        group_box.setChecked(False)

        self.shutter_l = QtWidgets.QLabel("Shutter:", self)
        self.shutter_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.close_open_filter_wheel = QtWidgets.QComboBox(self)
        self.close_open_filter_wheel.setMaximumWidth(100)
        self.fill_combo_close_open_filter_wheel_shutter()

        self.get_filter_l = QtWidgets.QLabel('Current filter:', self)
        self.filter_position = QtWidgets.QLabel(self.roda_filtros.get_current_filter())
        self.filter_position.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.filter_position.setMinimumWidth(60)

        self.btn_set_filter = QtWidgets.QPushButton('Set filter', self)
        self.set_filter_position = QtWidgets.QComboBox(self)
        self.set_filter_position.setMaximumWidth(100)
        self.fill_combo_filter_position()

        self.btn_home_position_filter = QtWidgets.QPushButton('Home Reset', self)

        group_box.setLayout(set_lvbox(set_hbox(self.shutter_l, self.close_open_filter_wheel), 
                                      set_hbox(self.get_filter_l, self.filter_position, stretch2=1), 
                                      set_hbox(self.btn_set_filter, self.set_filter_position), 
                                      set_hbox(self.btn_home_position_filter)))
        return group_box

    def create_ccd_info_group(self):
        group_box = QGroupBox("Info CCD")

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

        group_box.setLayout(set_lvbox(set_hbox(self.info_port_ccd_l, self.info_port_ccd_f),
                                      set_hbox(self.info_camera_model_l, self.info_camera_model_f),
                                      set_hbox(self.info_pixel_array_l, self.info_pixel_array_f)))
        return group_box

    def create_ccd_camera_group(self):
        group_box = QGroupBox("Settings")
        group_box.setCheckable(True)
        group_box.setChecked(False)

        self.shutter_l = QtWidgets.QLabel("Shutter:", self)
        self.shutter_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.close_open = QtWidgets.QComboBox(self)
        self.close_open.setMaximumWidth(100)
        self.fill_combo_close_open_ccd_shutter()

        self.temp_set_point_l = QtWidgets.QLabel("CCD Temp Set Point (°C):", self)
        self.temp_set_point_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.temp_set_point_f = QtWidgets.QLineEdit(self)
        self.temp_set_point_f.setMaximumWidth(100)

        self.temp_init_l = QtWidgets.QLabel("Tempo para iniciar(s):", self)
        self.temp_init_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.temp_init_f = QtWidgets.QLineEdit(self)
        self.temp_init_f.setMaximumWidth(100)

        self.btn_one_photo = QtWidgets.QPushButton('Take Photo', self)

        self.tempButton = QtWidgets.QPushButton("Set Temp", self)

        self.fanButton = QtWidgets.QPushButton("Fan (On/Off)")

        self.setting_values()

        group_box.setLayout(set_lvbox(set_hbox(self.shutter_l, self.close_open),
                                      set_hbox(self.temp_set_point_l, self.temp_set_point_f),
                                      set_hbox(self.temp_init_l, self.temp_init_f),
                                      set_hbox(self.btn_one_photo, self.tempButton, self.fanButton, stretch2=1)))
        return group_box

    def create_push_button_group(self):
        group_box = QGroupBox("&Push Buttons")
        # group_box.setCheckable(True)
        # group_box.setChecked(True)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.button_ok_func)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.func_cancel)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clear_all)

        group_box.setLayout(set_lvbox(set_hbox(self.saveButton, self.clearButton, self.cancelButton)))

        return group_box

    def get_info_pixels(self):
        # Function to get the CCD Info
        # This function will return [Pixels]

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
        self.close_open_filter_wheel.addItem("Open", 1)
        self.close_open_filter_wheel.addItem("Close", 2)
        self.close_open_filter_wheel.currentIndexChanged[str].connect(self.my_slot_close_open_shutter)

    def my_slot_close_open_shutter(self, item):
        if item == "Close":
            self.roda_filtros.close_shutter()
        else:
            self.roda_filtros.open_shutter()

    def fill_combo_filter_position(self):
            self.set_filter_position.addItem("1", 1)
            self.set_filter_position.addItem("2", 2)
            self.set_filter_position.addItem("3", 3)
            self.set_filter_position.addItem("4", 4)
            self.set_filter_position.addItem("5", 5)
            self.set_filter_position.addItem("6", 6)

    def func_filter_position(self):
        try:
            sleep(1)
            wish_filter_int = self.set_filter_position.currentIndex() + 1
            self.roda_filtros.filter_wheel_control(wish_filter_int)
            sleep(1)
        except Exception as e:
            print(e)
        finally:
            self.filter_position.setText(str(wish_filter_int))

    def button_settings(self):
        self.btn_set_filter.clicked.connect(self.func_filter_position)
        self.btn_home_position_filter.clicked.connect(self.func_home_position)

    def func_home_position(self):
        try:
            sleep(0.5)
            print("Home Position")
            self.roda_filtros.home_reset()
            sleep(1)
        except Exception as e:
            print(e)
        finally:
            self.filter_position.setText("1")

    def get_values(self):
        return self.var_save_ini_camera.get_camera_settings()

    def setting_values(self):
        info = self.get_values()
        self.set_values(info[0], info[1], info[2])

    def set_values(self, temperature_camera, temp_init_f, dark_photo):
        self.temp_set_point_f.setText(temperature_camera)
        try:
            open_or_close = int(dark_photo)
        except TypeError:
            open_or_close = 0
        self.temp_init_f.setText(temp_init_f)
        self.close_open.setCurrentIndex(open_or_close)

    def button_ok_func(self):
        try:
            self.var_save_ini_camera.set_camera_settings(self.temp_set_point_f.text(),
                                                         self.temp_init_f.text(), 
                                                         self.close_open.currentIndex())
            self.var_save_ini_camera.save_settings()
            self.console.raise_text("Camera settings successfully saved!", 1)

        except Exception as e:
            print(e)

    def clear_all(self):
        self.temp_set_point_f.clear()
        self.temp_init_f.clear()

    def func_cancel(self):
        self.imager_window.close()
