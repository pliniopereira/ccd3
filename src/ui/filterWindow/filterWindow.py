from PyQt5 import QtCore
from PyQt5 import QtWidgets

from src.business.filters.settingsFilters import SettingsFilters
from src.ui.commons.layout import set_lvbox, set_hbox
from src.business.consoleThreadOutput import ConsoleThreadOutput


class FilterWindow(QtWidgets.QWidget):
    '''
    Cria os campos e espaços no menu filter window
    '''
    def __init__(self, parent=None):
        super(FilterWindow, self).__init__(parent)
        self.create_filters_widgets()
        self.var_save_ini_filters = SettingsFilters()
        self.f = parent

        self.console = ConsoleThreadOutput()

        self.setLayout(set_lvbox(set_hbox(self.setField_label_label, self.setField_wavelength_label,
                                          self.setField_exposure_label, self.setField_binning_label,
                                          self.setField_ccdgain_label),
                                 set_hbox(self.setField_1, self.setField_label_filter1, self.setField_wavelength_filter1,
                                          self.setField_exposure_filter1, self.setField_binning_filter1,
                                          self.setField_ccdgain_filter1),
                                 set_hbox(self.setField_2, self.setField_label_filter2, self.setField_wavelength_filter2,
                                          self.setField_exposure_filter2, self.setField_binning_filter2,
                                          self.setField_ccdgain_filter2),
                                 set_hbox(self.setField_3, self.setField_label_filter3, self.setField_wavelength_filter3,
                                          self.setField_exposure_filter3, self.setField_binning_filter3,
                                          self.setField_ccdgain_filter3),
                                 set_hbox(self.setField_4, self.setField_label_filter4, self.setField_wavelength_filter4,
                                          self.setField_exposure_filter4, self.setField_binning_filter4,
                                          self.setField_ccdgain_filter4),
                                 set_hbox(self.setField_5, self.setField_label_filter5, self.setField_wavelength_filter5,
                                          self.setField_exposure_filter5, self.setField_binning_filter5,
                                          self.setField_ccdgain_filter5),
                                 set_hbox(self.setField_6, self.setField_label_filter6, self.setField_wavelength_filter6,
                                          self.setField_exposure_filter6, self.setField_binning_filter6,
                                          self.setField_ccdgain_filter6),
                                 set_hbox(self.buttonok, self.button_clear, self.buttoncancel, stretch2=1)))

    def get_values(self):
        return self.var_save_ini_filters.SettingsFilters()

    def setting_values(self):
        info = self.get_values()
        self.set_values(info[0])

    def set_values(self, x):
        self.setField_x.setText(x)

    def create_filters_widgets(self):
        self.setField_label_label = QtWidgets.QLabel("    Label", self)
        self.setField_wavelength_label = QtWidgets.QLabel("Wavelength (nm)", self)
        self.setField_exposure_label = QtWidgets.QLabel("Exposure (ms)", self)
        self.setField_binning_label =  QtWidgets.QLabel("Binning", self)
        self.setField_ccdgain_label =  QtWidgets.QLabel("CCD Gain", self)

        self.setField_1 = QtWidgets.QLabel("1", self)
        self.setField_2 = QtWidgets.QLabel("2", self)
        self.setField_3 = QtWidgets.QLabel("3", self)
        self.setField_4 = QtWidgets.QLabel("4", self)
        self.setField_5 = QtWidgets.QLabel("5", self)
        self.setField_6 = QtWidgets.QLabel("6", self)

        self.setField_label_filter1 = QtWidgets.QLineEdit(self)
        self.setField_label_filter2 = QtWidgets.QLineEdit(self)
        self.setField_label_filter3 = QtWidgets.QLineEdit(self)
        self.setField_label_filter4 = QtWidgets.QLineEdit(self)
        self.setField_label_filter5 = QtWidgets.QLineEdit(self)
        self.setField_label_filter6 = QtWidgets.QLineEdit(self)

        self.setField_wavelength_filter1 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter2 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter3 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter4 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter5 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter6 = QtWidgets.QLineEdit(self)

        self.setField_exposure_filter1 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter2 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter3 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter4 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter5 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter6 = QtWidgets.QLineEdit(self)

        self.setField_binning_filter1 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter2 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter3 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter4 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter5 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter6 = QtWidgets.QLineEdit(self)

        self.setField_ccdgain_filter1 = QtWidgets.QLineEdit(self)
        self.setField_ccdgain_filter2 = QtWidgets.QLineEdit(self)
        self.setField_ccdgain_filter3 = QtWidgets.QLineEdit(self)
        self.setField_ccdgain_filter4 = QtWidgets.QLineEdit(self)
        self.setField_ccdgain_filter5 = QtWidgets.QLineEdit(self)
        self.setField_ccdgain_filter6 = QtWidgets.QLineEdit(self)

        self.buttonok = QtWidgets.QPushButton("Save", self)
        self.buttonok.clicked.connect(self.button_ok_func)

        self.button_clear = QtWidgets.QPushButton('Clear', self)
        self.button_clear.clicked.connect(self.clear_all)

        self.buttoncancel = QtWidgets.QPushButton("Cancel", self)
        self.buttoncancel.clicked.connect(self.func_cancel)

    def button_ok_func(self):
        try:
            self.var_save_ini_filters.set_filters_settings(self.setField_x.text())
            self.var_save_ini_filters.save_settings()
            self.console.raise_text("Filters settings successfully saved!", 1)
        except Exception as e:
            print(e)

    def clear_all(self):
        self.setField_label_filter1.clear()
        self.setField_label_filter2.clear()
        self.setField_label_filter3.clear()
        self.setField_label_filter4.clear()
        self.setField_label_filter5.clear()
        self.setField_label_filter6.clear()

        self.setField_wavelength_filter1.clear()
        self.setField_wavelength_filter2.clear()
        self.setField_wavelength_filter3.clear()
        self.setField_wavelength_filter4.clear()
        self.setField_wavelength_filter5.clear()
        self.setField_wavelength_filter6.clear()

        self.setField_exposure_filter1.clear()
        self.setField_exposure_filter2.clear()
        self.setField_exposure_filter3.clear()
        self.setField_exposure_filter4.clear()
        self.setField_exposure_filter5.clear()
        self.setField_exposure_filter6.clear()

        self.setField_binning_filter1.clear()
        self.setField_binning_filter2.clear()
        self.setField_binning_filter3.clear()
        self.setField_binning_filter4.clear()
        self.setField_binning_filter5.clear()
        self.setField_binning_filter6.clear()

        self.setField_ccdgain_filter1.clear()
        self.setField_ccdgain_filter2.clear()
        self.setField_ccdgain_filter3.clear()
        self.setField_ccdgain_filter4.clear()
        self.setField_ccdgain_filter5.clear()
        self.setField_ccdgain_filter6.clear()

    def func_cancel(self):
        self.f.close()
