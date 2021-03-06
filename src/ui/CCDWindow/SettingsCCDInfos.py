from time import sleep

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QPushButton, QWidget

from src.business.configuration.settingsCamera import SettingsCamera
from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.shooters.InfosForSThread import get_filter_settings
from src.business.shooters.SThread import SThread
from src.controller.Camera import Camera
from src.controller.commons.Locker import Locker
from src.controller.fan import Fan
from src.ui.commons.layout import set_hbox, set_lvbox
from src.utils.camera.SbigDriver import (ccdinfo, getlinkstatus)
from src.utils.rodafiltros.FilterControl import FilterControl


class SettingsCCDInfos(QWidget):
    def __init__(self, parent=None):
        super(SettingsCCDInfos, self).__init__(parent)

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
        self.close_open_filter_wheel_info = None
        self.btn_set_shutter = None
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
        self.one_photoButton = None
        self.tempButton = None
        self.fanButton = None

        # Instance attributes create_push_button_group
        self.saveButton = None
        self.cancelButton = None
        self.clearButton = None

        self.select_filter_manual = 1
        self.select_filter_shutter = "Closed"

        self.imager_window = parent

        self.cam = Camera()

        self.roda_filtros = FilterControl()

        self.var_save_ini_camera = SettingsCamera()

        self.console = ConsoleThreadOutput()

        self.fan = Fan(self.fanButton)

        self.one_photo = SThread()

        self.lock = Locker()

        self.firmware = "????"
        self.model = "????"
        self.y_pixels = "????"
        self.x_pixels = "????"

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
        self.info_cam()

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
        self.shutter_l = QtWidgets.QLabel("Shutter status:", self)
        self.shutter_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.close_open_filter_wheel_info = QtWidgets.QLabel("Closed")
        self.close_open_filter_wheel_info.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.btn_set_shutter = QtWidgets.QPushButton('Set shutter', self)
        self.close_open_filter_wheel = QtWidgets.QComboBox(self)
        self.close_open_filter_wheel.setMaximumWidth(100)
        self.fill_combo_close_open_filter_wheel_shutter()

        filter_position = self.roda_filtros.get_current_filter()

        if filter_position == "None":
            filter_position = "1"

        self.get_filter_l = QtWidgets.QLabel('Current filter:', self)
        self.filter_position = QtWidgets.QLabel(filter_position)
        self.filter_position.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.filter_position.setMinimumWidth(60)

        self.btn_set_filter = QtWidgets.QPushButton('Set filter', self)
        self.set_filter_position = QtWidgets.QComboBox(self)
        self.set_filter_position.setMaximumWidth(100)
        self.fill_combo_filter_position()

        self.btn_home_position_filter = QtWidgets.QPushButton('Home Reset', self)

        group_box.setLayout(set_lvbox(set_hbox(self.shutter_l, self.close_open_filter_wheel_info),
                                      set_hbox(self.btn_set_shutter, self.close_open_filter_wheel),
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
        self.close_open = QtWidgets.QLabel("Closed")
        self.close_open.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.temp_set_point_l = QtWidgets.QLabel("CCD Temp Set Point (°C):", self)
        self.temp_set_point_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.temp_set_point_f = QtWidgets.QLineEdit(self)
        self.temp_set_point_f.setMaximumWidth(100)
        self.temp_set_point_f.setValidator(QIntValidator(-100, 30))

        self.temp_init_l = QtWidgets.QLabel("Tempo para iniciar(s):", self)
        self.temp_init_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.temp_init_f = QtWidgets.QLineEdit(self)
        self.temp_init_f.setMaximumWidth(100)
        self.temp_init_f.setValidator(QIntValidator(0, 600))

        self.one_photoButton = QtWidgets.QPushButton('Take Photo', self)
        self.one_photoButton.clicked.connect(self.take_one_photo)

        self.tempButton = QtWidgets.QPushButton("Set Temp", self)
        self.tempButton.clicked.connect(self.btn_temperature)

        self.fanButton = QtWidgets.QPushButton("Fan (On/Off)")
        self.fanButton.clicked.connect(self.button_fan_func)

        self.setting_values()

        group_box.setLayout(set_lvbox(set_hbox(self.shutter_l, self.close_open),
                                      set_hbox(self.temp_set_point_l, self.temp_set_point_f),
                                      set_hbox(self.temp_init_l, self.temp_init_f),
                                      set_hbox(self.one_photoButton, self.tempButton, self.fanButton, stretch2=1)))
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

    def fill_combo_close_open_filter_wheel_shutter(self):
        self.close_open_filter_wheel.addItem("Closed", 2)
        self.close_open_filter_wheel.addItem("Opened", 1)

    def func_close_open_shutter(self):
        my_slot_close_open_shutter = self.close_open_filter_wheel.currentIndex()

        if my_slot_close_open_shutter == 0:
            self.roda_filtros.close_shutter()
            self.select_filter_shutter = "Closed"
            self.console.raise_text("Shutter Filter Wheel Closed", 1)
            self.close_open.setText("Closed")
            self.close_open_filter_wheel_info.setText("Closed")
        else:
            self.roda_filtros.open_shutter()
            self.select_filter_shutter = "Opened"
            self.console.raise_text("Shutter Filter Wheel Opened ", 1)
            self.close_open.setText("Opened")
            self.close_open_filter_wheel_info.setText("Opened")

    def fill_combo_filter_position(self):
        self.set_filter_position.addItem("1", 1)
        self.set_filter_position.addItem("2", 2)
        self.set_filter_position.addItem("3", 3)
        self.set_filter_position.addItem("4", 4)
        self.set_filter_position.addItem("5", 5)
        self.set_filter_position.addItem("6", 6)

    def func_filter_position(self):
        available_filters_list_and_commons = get_filter_settings()
        available_filters_list_and_commons = list(available_filters_list_and_commons)

        permited_filters = ''

        for x in available_filters_list_and_commons:
            permited_filters += str(x)

        try:
            if self.roda_filtros.connect_state:
                sleep(1)
                wish_filter_int = self.set_filter_position.currentIndex() + 1
                aux = 1
                for x in permited_filters:
                    if int(wish_filter_int) == int(x):
                        aux = 0

                if aux == 0:
                    self.roda_filtros.filter_wheel_control(int(wish_filter_int))
                else:
                    self.console.raise_text("There is no filter on slot number " + str(wish_filter_int) + "!", 3)
                    self.console.raise_text("Please include a new filter on the Filters Settings Menu!", 3)

                sleep(1)
        except Exception as e:
            print("def func_filter_position(self): -> " + str(e))

        finally:
            if aux == 0:
                if self.roda_filtros.connect_state:
                    self.select_filter_manual = wish_filter_int

                    self.filter_position.setText(str(wish_filter_int))
                    self.console.raise_text("Filter Position: {}".format(str(wish_filter_int)), 2)
                else:
                    self.filter_position.setText("?")
                    self.console.raise_text("Filter Wheel is not connect!", 3)

    def button_settings(self):
        self.btn_set_shutter.clicked.connect(self.func_close_open_shutter)
        self.btn_set_filter.clicked.connect(self.func_filter_position)
        self.btn_home_position_filter.clicked.connect(self.func_home_position)

    def func_home_position(self):
        try:
            if self.roda_filtros.connect_state:
                sleep(0.5)
                print("Home Position")
                self.roda_filtros.home_reset()
                sleep(1)
        except Exception as e:
            print(e)
        finally:
            if self.roda_filtros.connect_state:
                self.filter_position.setText("1")
                self.console.raise_text("Filter Position: 1", 2)
                self.console.raise_text("Shutter Filter Wheel Closed", 1)
                self.close_open.setText("Closed")
                self.close_open_filter_wheel_info.setText("Closed")
            else:
                self.filter_position.setText("?")
                self.console.raise_text("Filter Wheel is not connect!", 3)

    def get_values(self):
        return self.var_save_ini_camera.get_camera_settings()

    def setting_values(self):
        info = self.get_values()
        self.set_values(info[0], info[1])

    def set_values(self, temperature_camera, temp_init_f):
        self.temp_set_point_f.setText(temperature_camera)
        self.temp_init_f.setText(temp_init_f)

    def button_ok_func(self):
        try:
            self.var_save_ini_camera.set_camera_settings(self.temp_set_point_f.text(),
                                                         self.temp_init_f.text())

            self.var_save_ini_camera.save_settings()
            self.console.raise_text("Camera settings successfully saved!", 1)

        except Exception as e:
            print(e)

    def clear_all(self):
        self.temp_set_point_f.clear()
        self.temp_init_f.clear()

    def func_cancel(self):
        self.imager_window.close()

    def take_one_photo(self):
        try:
            if self.select_filter_shutter == "Closed":
                self.console.raise_text("AQUI dark photo", 1)
                self.cam.start_one_photo(self.select_filter_manual, self.select_filter_shutter)
                # self.one_photo.args_one_photo(self.select_filter_manual, self.select_filter_shutter)
                # self.one_photo.start()
            else:
                self.console.raise_text("AQUI photo", 1)
                self.cam.start_one_photo(self.select_filter_manual, self.select_filter_shutter)
        except Exception as e:
            self.console.raise_text("Not possible taking photo -> {}".format(e), 1)

    def button_fan_func(self):
        if getlinkstatus() is True:
            try:
                self.fan.set_fan()
                self.console.raise_text('State changed Fan!', 2)
            except Exception as e:
                self.console.raise_text("The camera is not connected!", 3)
                self.console.raise_text('State Fan unchanged', 3)
                self.console.raise_text("Exception -> {}".format(e))
        else:
            self.console.raise_text("The camera is not connected!", 3)
            self.console.raise_text('State Fan unchanged', 3)

    def btn_temperature(self):
        try:
            value = self.temp_set_point_f.text()
            if value is '':
                pass
            else:
                try:
                    self.cam.set_temperature(float(value))
                except TypeError:
                    self.cam.set_temperature(float(20.0))
        except Exception as e:
            print("Exception -> {}".format(e))

    def info_cam(self):
        try:
            if getlinkstatus() is True:
                self.firmware, self.model, self.y_pixels, self.x_pixels = \
                    self.cam.get_firmware_and_model_and_pixels()
            else:
                self.firmware, self.model, self.y_pixels, self.x_pixels = "????", "????", \
                                                                          "????", "????"

            self.info_port_ccd_f.setText(self.firmware)
            self.info_camera_model_f.setText(self.model)
            self.info_pixel_array_f.setText(str(self.y_pixels) + " x " + str(self.x_pixels))

        except Exception as e:
            print("CCDInfos get_firmware_and_model_and_pixels -> {}".format(e))
            self.firmware, self.model, self.y_pixels, self.x_pixels = "????", "????", \
                                                                      "????", "????"
