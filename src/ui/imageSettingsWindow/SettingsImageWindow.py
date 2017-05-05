from src.business.configuration.settingsCamera import SettingsCamera
from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.shooters.SThread import SThread
from src.controller.camera import Camera
from src.controller.commons.Locker import Locker
from src.controller.fan import Fan
from src.ui.commons.layout import set_lvbox, set_hbox
from src.utils.camera.SbigDriver import (ccdinfo, getlinkstatus)

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QPushButton, QVBoxLayout, QWidget)

from src.ui.commons.layout import set_lvbox, set_hbox
from src.utils.camera.SbigDriver import (ccdinfo, getlinkstatus)


class SettingsImageWindow(QtWidgets.QWidget):
    '''
    Cria os campos e espaços no menu settings window
    '''
    def __init__(self, parent=None):
        super(SettingsImageWindow, self).__init__(parent)
        self.cam = SettingsCamera()
        self.camera = Camera()
        self.console = ConsoleThreadOutput()
        self.p = parent

        self.lock = Locker()

        self.one_photo = SThread()

        grid = QGridLayout()
        grid.addWidget(self.createImageContrastGroup(), 2, 0)
        grid.addWidget(self.createCropGroup(), 3, 0)
        grid.addWidget(self.createTypeImageGroup(), 4, 0)
        grid.addWidget(self.createPushButtonGroup(), 5, 0)
        self.setLayout(grid)

        self.setWindowTitle("Imager Box")

    def get_camera_settings(self):
        settings = SettingsCamera()
        info = settings.get_camera_settings()
        return info

    def get_pixels(self):
        info = self.get_info_pixels()
        return int(info[-2]), int(info[-1])

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

    def createImageContrastGroup(self):
        groupBox = QGroupBox("&Image Contrast:")
        groupBox.setCheckable(True)
        groupBox.setChecked(True)

        self.getlevel1 = QtWidgets.QLabel("Bottom Level:", self)
        self.getlevel1.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getlevel1l = QtWidgets.QLineEdit(self)
        self.getlevel1l.setMaximumWidth(50)

        self.getlevel2 = QtWidgets.QLabel("Top Level:", self)
        self.getlevel2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getlevel2l = QtWidgets.QLineEdit(self)
        self.getlevel2l.setMaximumWidth(50)

        groupBox.setLayout(set_lvbox(set_hbox(self.getlevel1, self.getlevel1l, self.getlevel2, self.getlevel2l)))

        return groupBox

    def createCropGroup(self):
        groupBox = QGroupBox("&Crop")
        groupBox.setCheckable(True)
        groupBox.setChecked(False)

        self.ignore_crop_l = QtWidgets.QCheckBox('Ignore Crop Image', self)

        self.crop_msg = QtWidgets.QLabel("Crop Image", self)
        self.crop_xi = QtWidgets.QLabel("Width: Wi:", self)
        self.crop_xi.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getcropxi_l = QtWidgets.QLineEdit(self)
        self.getcropxi_l.setMaximumWidth(50)

        self.crop_xf = QtWidgets.QLabel("Wf:", self)
        self.crop_xf.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getcropxf_l = QtWidgets.QLineEdit(self)
        self.getcropxf_l.setMaximumWidth(50)

        self.crop_yi = QtWidgets.QLabel("Height: Hi:", self)
        self.crop_yi.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getcropyi_l = QtWidgets.QLineEdit(self)
        self.getcropyi_l.setMaximumWidth(50)

        self.crop_yf = QtWidgets.QLabel("Hf:", self)
        self.crop_yf.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getcropyf_l = QtWidgets.QLineEdit(self)
        self.getcropyf_l.setMaximumWidth(50)

        groupBox.setLayout(set_lvbox(set_hbox(self.ignore_crop_l),
                                     set_hbox(self.crop_msg),
                                     set_hbox(self.crop_xi, self.getcropxi_l, self.crop_xf, self.getcropxf_l),
                                     set_hbox(self.crop_yi, self.getcropyi_l, self.crop_yf, self.getcropyf_l)))

        return groupBox


    def createTypeImageGroup(self):
        groupBox = QGroupBox("&File to save")
        groupBox.setCheckable(True)
        groupBox.setChecked(True)

        self.image_tif_l = QtWidgets.QCheckBox('Image .tif', self)
        self.image_fit_l = QtWidgets.QCheckBox('Image .fit', self)

        groupBox.setLayout(set_lvbox(set_hbox(self.image_tif_l),
                                     set_hbox(self.image_fit_l)))

        return groupBox

    def createPushButtonGroup(self):
        groupBox = QGroupBox()
        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")
        self.clearButton = QPushButton("Clear")

        groupBox.setLayout(set_lvbox(set_hbox(self.saveButton, self.clearButton, self.cancelButton)))

        return groupBox

    def button_ok_func(self):
        try:
            y_pixels, x_pixels = self.get_pixels()

            # Saving the Settings
            if int(self.getcropxi_l.text()) > int(self.getcropxf_l.text()) or\
                            int(self.getcropyi_l.text()) > int(self.getcropyf_l.text()) or\
                            int(self.getcropxf_l.text()) >= x_pixels/(int(self.combo.currentIndex() + 1)) or \
                            int(self.getcropyf_l.text()) >= y_pixels/(int(self.combo.currentIndex() + 1)):
                self.console.raise_text("Wrong values for image crop.", 3)
            else:
                self.cam.set_camera_settings(self.setField_temperature.text(), self.prel.text(), self.expl.text(),
                                         self.combo.currentIndex(), self.tempo_fotos.text(), self.time_colling.text(),
                                         self.getlevel1l.text(), self.getlevel2l.text(), self.close_open.currentIndex(),
                                         self.getcropxi_l.text(), self.getcropxf_l.text(),
                                         self.getcropyi_l.text(), self.getcropyf_l.text(),
                                         self.ignore_crop_l.isChecked())
                self.cam.save_settings()
                self.console.raise_text("Camera settings successfully saved!", 1)
        except Exception as e:
            self.console.raise_text("Camera settings were not saved.", 3)

    def clear_all(self):
        self.setField_temperature.clear()
        self.prel.clear()
        self.expl.clear()
        self.tempo_fotos.clear()

    def take_one_photo(self):
        try:
            info = self.get_camera_settings()
            if int(info[8]) == 1:
                self.console.raise_text("Taking dark photo", 1)
                self.one_photo.start()
            else:
                self.console.raise_text("Taking photo", 1)
                self.one_photo.start()
        except Exception:
            self.console.raise_text("Not possible taking photo", 1)

    def func_cancel(self):
        self.p.close()

    def button_fan_func(self):
        if getlinkstatus() is True:
            try:
                self.fan.set_fan()
                self.console.raise_text('State changed Fan!', 2)
            except Exception:
                self.console.raise_text("The camera is not connected!", 3)
                self.console.raise_text('State Fan unchanged', 3)
        else:
            self.console.raise_text("The camera is not connected!", 3)
            self.console.raise_text('State Fan unchanged', 3)

    def fill_combo(self):
        self.combo.addItem("1x1", 0)
        self.combo.addItem("2x2", 1)
        self.combo.addItem("3x3", 2)

    def fill_combo_close_open(self):
        self.close_open.addItem("Open", 0)
        self.close_open.addItem("Close", 1)

    def btn_temperature(self):
            try:
                value = self.setField_temperature.text()
                if value is '':
                    pass
                else:
                    self.camera.set_temperature(float(value))
            except Exception as e:
                print("Exception -> {}".format(e))
