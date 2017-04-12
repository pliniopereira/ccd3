from PyQt5 import QtCore
from PyQt5 import QtWidgets

from src.business.filters.settingsFilters import SettingsFilters
from src.ui.commons.layout import set_lvbox, set_hbox


class FilterWindow(QtWidgets.QWidget):
    '''
    Cria os campos e espaços no menu filter window
    '''
    def __init__(self, parent=None):
        super(FilterWindow, self).__init__(parent)
        self.create_filters_widgets()
        self.var_save_ini_filters = SettingsFilters()


        self.setLayout(set_lvbox(set_hbox(self.setField_temperature_label, self.setField_temperature),
                                 set_hbox(self.pre, self.prel),
                                 set_hbox(self.exp, self.expl),
                                 set_hbox(self.binning, self.combo),
                                 set_hbox(self.dark, self.close_open),
                                 set_hbox(self.tempo_fotos_label, self.tempo_fotos),
                                 set_hbox(self.time_colling_label, self.time_colling),
                                 set_hbox(self.contrast_msg),
                                 set_hbox(self.getlevel1, self.getlevel1l, self.getlevel2, self.getlevel2l),
                                 set_hbox(self.ignore_crop_l),
                                 set_hbox(self.crop_msg),
                                 set_hbox(self.crop_xi, self.getcropxi_l, self.crop_xf, self.getcropxf_l),
                                 set_hbox(self.crop_yi, self.getcropyi_l, self.crop_yf, self.getcropyf_l),
                                 set_hbox(self.buttonok, self.button_clear, self.buttoncancel, stretch2=1)))

    def get_values(self):
        return self.var_save_ini_filters.SettingsFilters()

    def setting_values(self):
        info = self.get_values()
        self.set_values(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9],\
                        info[10], info[11], info[12], info[13])

    def set_values(self, temperature_camera, prefixo, exposicao, binning, tempo_entre_fotos, time_colling, get_level1,\
                   get_level2, dark_photo, crop_xi, crop_xf, crop_yi, crop_yf, ignore_crop):
        self.setField_temperature.setText(temperature_camera)
        self.prel.setText(prefixo)
        self.expl.setText(exposicao)

        try:
            b = int(binning)
        except:
            b = 0

        try:
            open_or_close = int(dark_photo)
        except:
            open_or_close = 0

        self.tempo_fotos.setText(tempo_entre_fotos)
        self.time_colling.setText(time_colling)
        self.combo.setCurrentIndex(b)
        self.close_open.setCurrentIndex(open_or_close)

        self.getlevel1l.setText(get_level1)
        self.getlevel2l.setText(get_level2)

        self.getcropxi_l.setText(crop_xi)
        self.getcropxf_l.setText(crop_xf)
        self.getcropyi_l.setText(crop_yi)
        self.getcropyf_l.setText(crop_yf)

        self.ignore_crop_l.setChecked(ignore_crop)

    def create_filters_widgets(self):
        self.setField_temperature_label = QtWidgets.QLabel("TESTE", self)
        self.setField_temperature_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.setField_temperature = QtWidgets.QLineEdit(self)
        self.setField_temperature.setMaximumWidth(100)

        self.pre = QtWidgets.QLabel("TESTE", self)
        self.pre.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.prel = QtWidgets.QLineEdit(self)
        self.prel.setMaximumWidth(100)

        self.exp = QtWidgets.QLabel("TESTE", self)
        self.exp.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.expl = QtWidgets.QLineEdit(self)
        self.expl.setMaximumWidth(100)

        self.binning = QtWidgets.QLabel("TESTE", self)
        self.binning.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.combo = QtWidgets.QComboBox(self)
        self.combo.setMaximumWidth(100)

        self.dark = QtWidgets.QLabel("TESTE", self)
        self.dark.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.close_open = QtWidgets.QComboBox(self)
        self.close_open.setMaximumWidth(100)

        self.tempo_fotos_label = QtWidgets.QLabel("TESTE", self)
        self.tempo_fotos_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.tempo_fotos = QtWidgets.QLineEdit(self)
        self.tempo_fotos.setMaximumWidth(100)

        self.time_colling_label = QtWidgets.QLabel("TESTE", self)
        self.time_colling_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.time_colling = QtWidgets.QLineEdit(self)
        self.time_colling.setMaximumWidth(100)

        self.contrast_msg = QtWidgets.QLabel("TESTE", self)
        self.getlevel1 = QtWidgets.QLabel("TESTE", self)
        self.getlevel1.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getlevel1l = QtWidgets.QLineEdit(self)
        self.getlevel1l.setMaximumWidth(50)

        self.getlevel2 = QtWidgets.QLabel("Top Level:", self)
        self.getlevel2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.getlevel2l = QtWidgets.QLineEdit(self)
        self.getlevel2l.setMaximumWidth(50)

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

        self.button_clear = QtWidgets.QPushButton('Clear', self)
        self.button_clear.clicked.connect(self.clear_all)

        self.btn_one_photo = QtWidgets.QPushButton('Take Photo', self)

        self.tempButton = QtWidgets.QPushButton("Set Temp", self)

        self.fanButton = QtWidgets.QPushButton("Fan (On/Off)")

        self.buttonok = QtWidgets.QPushButton("Save", self)
        self.buttonok.clicked.connect(self.button_ok_func)

        self.buttoncancel = QtWidgets.QPushButton("Cancel", self)
        self.buttoncancel.clicked.connect(self.func_cancel)

    def button_ok_func(self):
        try:
            self.var_save_ini_filters.save_settings()
            self.console.raise_text("Camera settings successfully saved!", 1)
        except Exception as e:
            self.console.raise_text("Camera settings were not saved.", 3)

    def clear_all(self):
        self.setField_temperature.clear()
        self.prel.clear()
        self.expl.clear()
        self.tempo_fotos.clear()

    def func_cancel(self):
        self.f.close()
