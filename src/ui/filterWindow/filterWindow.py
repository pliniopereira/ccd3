from PyQt5 import QtWidgets

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.filters.settingsFilters import SettingsFilters
from src.ui.commons.layout import set_lvbox, set_hbox


class FilterWindow(QtWidgets.QWidget):
    # Cria os campos e espaços no menu filter window

    def __init__(self, parent=None):
        super(FilterWindow, self).__init__(parent)
        self.create_filters_widgets()
        self.var_save_ini_filters = SettingsFilters()
        self.f = parent

        self.console = ConsoleThreadOutput()

        self.setting_values()

        self.setLayout(set_lvbox(set_hbox(self.setField_label_label, self.setField_wavelength_label,
                                          self.setField_exposure_label, self.setField_binning_label,
                                          self.setField_ccdgain_label),
                                 set_hbox(self.setField_1, self.setField_label_filter1,
                                          self.setField_wavelength_filter1, self.setField_exposure_filter1,
                                          self.setField_binning_filter1, self.setField_ccdgain_filter1),
                                 set_hbox(self.setField_2, self.setField_label_filter2,
                                          self.setField_wavelength_filter2, self.setField_exposure_filter2,
                                          self.setField_binning_filter2, self.setField_ccdgain_filter2),
                                 set_hbox(self.setField_3, self.setField_label_filter3,
                                          self.setField_wavelength_filter3, self.setField_exposure_filter3,
                                          self.setField_binning_filter3, self.setField_ccdgain_filter3),
                                 set_hbox(self.setField_4, self.setField_label_filter4,
                                          self.setField_wavelength_filter4, self.setField_exposure_filter4,
                                          self.setField_binning_filter4, self.setField_ccdgain_filter4),
                                 set_hbox(self.setField_5, self.setField_label_filter5,
                                          self.setField_wavelength_filter5, self.setField_exposure_filter5,
                                          self.setField_binning_filter5, self.setField_ccdgain_filter5),
                                 set_hbox(self.setField_6, self.setField_label_filter6,
                                          self.setField_wavelength_filter6, self.setField_exposure_filter6,
                                          self.setField_binning_filter6, self.setField_ccdgain_filter6),
                                 set_hbox(self.buttonok, self.button_clear, self.buttoncancel, stretch2=1)))

    def get_values(self):
        return self.var_save_ini_filters.get_filters_settings()

    def setting_values(self):
        info = self.get_values()
        self.set_values(info[0], info[1], info[2], info[3], info[4],
                        info[5], info[6], info[7], info[8], info[9], info[10],
                        info[11], info[12], info[13], info[14], info[15],
                        info[16], info[17], info[18], info[19], info[20],
                        info[21], info[22], info[23], info[24], info[25],
                        info[26], info[27], info[28], info[29])

    def set_values(self,
                   label_filter1, wavelength_filter1, exposure_filter1, binning_filter1, ccdgain_filter1,
                   label_filter2, wavelength_filter2, exposure_filter2, binning_filter2, ccdgain_filter2,
                   label_filter3, wavelength_filter3, exposure_filter3, binning_filter3, ccdgain_filter3,
                   label_filter4, wavelength_filter4, exposure_filter4, binning_filter4, ccdgain_filter4,
                   label_filter5, wavelength_filter5, exposure_filter5, binning_filter5, ccdgain_filter5,
                   label_filter6, wavelength_filter6, exposure_filter6, binning_filter6, ccdgain_filter6):
        binning_var1 = self.erro_binning(binning_filter1)
        binning_var2 = self.erro_binning(binning_filter2)
        binning_var3 = self.erro_binning(binning_filter3)
        binning_var4 = self.erro_binning(binning_filter4)
        binning_var5 = self.erro_binning(binning_filter5)
        binning_var6 = self.erro_binning(binning_filter6)

        self.setField_label_filter1.setText(label_filter1)
        self.setField_wavelength_filter1.setText(wavelength_filter1)
        self.setField_exposure_filter1.setText(exposure_filter1)
        self.setField_binning_filter1.setCurrentIndex(binning_var1)
        self.setField_ccdgain_filter1.setText(ccdgain_filter1)

        self.setField_label_filter2.setText(label_filter2)
        self.setField_wavelength_filter2.setText(wavelength_filter2)
        self.setField_exposure_filter2.setText(exposure_filter2)
        self.setField_binning_filter2.setCurrentIndex(binning_var2)
        self.setField_ccdgain_filter2.setText(ccdgain_filter2)

        self.setField_label_filter3.setText(label_filter3)
        self.setField_wavelength_filter3.setText(wavelength_filter3)
        self.setField_exposure_filter3.setText(exposure_filter3)
        self.setField_binning_filter3.setCurrentIndex(binning_var3)
        self.setField_ccdgain_filter3.setText(ccdgain_filter3)

        self.setField_label_filter4.setText(label_filter4)
        self.setField_wavelength_filter4.setText(wavelength_filter4)
        self.setField_exposure_filter4.setText(exposure_filter4)
        self.setField_binning_filter4.setCurrentIndex(binning_var4)
        self.setField_ccdgain_filter4.setText(ccdgain_filter4)

        self.setField_label_filter5.setText(label_filter5)
        self.setField_wavelength_filter5.setText(wavelength_filter5)
        self.setField_exposure_filter5.setText(exposure_filter5)
        self.setField_binning_filter5.setCurrentIndex(binning_var5)
        self.setField_ccdgain_filter5.setText(ccdgain_filter5)

        self.setField_label_filter6.setText(label_filter6)
        self.setField_wavelength_filter6.setText(wavelength_filter6)
        self.setField_exposure_filter6.setText(exposure_filter6)
        self.setField_binning_filter6.setCurrentIndex(binning_var6)
        self.setField_ccdgain_filter6.setText(ccdgain_filter6)

    def create_filters_widgets(self):
        self.setField_label_label = QtWidgets.QLabel("    Label", self)
        self.setField_wavelength_label = QtWidgets.QLabel("Wavelength (nm)", self)
        self.setField_exposure_label = QtWidgets.QLabel("Exposure (ms)", self)
        self.setField_binning_label = QtWidgets.QLabel("Binning", self)
        self.setField_ccdgain_label = QtWidgets.QLabel("CCD Gain", self)

        self.setField_1 = QtWidgets.QLabel("1", self)
        self.setField_2 = QtWidgets.QLabel("2", self)
        self.setField_3 = QtWidgets.QLabel("3", self)
        self.setField_4 = QtWidgets.QLabel("4", self)
        self.setField_5 = QtWidgets.QLabel("5", self)
        self.setField_6 = QtWidgets.QLabel("6", self)

        self.setField_label_filter1 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter1 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter1 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter1 = QtWidgets.QComboBox(self)
        self.setField_binning_filter1.addItem("1x1", 0)
        self.setField_binning_filter1.addItem("2x2", 1)
        self.setField_binning_filter1.addItem("3x3", 2)
        self.setField_ccdgain_filter1 = QtWidgets.QLineEdit(self)

        self.setField_label_filter2 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter2 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter2 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter2 = QtWidgets.QComboBox(self)
        self.setField_binning_filter2.addItem("1x1", 0)
        self.setField_binning_filter2.addItem("2x2", 1)
        self.setField_binning_filter2.addItem("3x3", 2)
        self.setField_ccdgain_filter2 = QtWidgets.QLineEdit(self)

        self.setField_label_filter3 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter3 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter3 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter3 = QtWidgets.QComboBox(self)
        self.setField_binning_filter3.addItem("1x1", 0)
        self.setField_binning_filter3.addItem("2x2", 1)
        self.setField_binning_filter3.addItem("3x3", 2)
        self.setField_ccdgain_filter3 = QtWidgets.QLineEdit(self)

        self.setField_label_filter4 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter4 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter4 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter4 = QtWidgets.QComboBox(self)
        self.setField_binning_filter4.addItem("1x1", 0)
        self.setField_binning_filter4.addItem("2x2", 1)
        self.setField_binning_filter4.addItem("3x3", 2)
        self.setField_ccdgain_filter4 = QtWidgets.QLineEdit(self)

        self.setField_label_filter5 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter5 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter5 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter5 = QtWidgets.QComboBox(self)
        self.setField_binning_filter5.addItem("1x1", 0)
        self.setField_binning_filter5.addItem("2x2", 1)
        self.setField_binning_filter5.addItem("3x3", 2)
        self.setField_ccdgain_filter5 = QtWidgets.QLineEdit(self)

        self.setField_label_filter6 = QtWidgets.QLineEdit(self)
        self.setField_wavelength_filter6 = QtWidgets.QLineEdit(self)
        self.setField_exposure_filter6 = QtWidgets.QLineEdit(self)
        self.setField_binning_filter6 = QtWidgets.QComboBox(self)
        self.setField_binning_filter6.addItem("1x1", 0)
        self.setField_binning_filter6.addItem("2x2", 1)
        self.setField_binning_filter6.addItem("3x3", 2)
        self.setField_ccdgain_filter6 = QtWidgets.QLineEdit(self)

        self.buttonok = QtWidgets.QPushButton("Save", self)
        self.buttonok.clicked.connect(self.button_ok_func)

        self.button_clear = QtWidgets.QPushButton('Clear', self)
        self.button_clear.clicked.connect(self.clear_all)

        self.buttoncancel = QtWidgets.QPushButton("Cancel", self)
        self.buttoncancel.clicked.connect(self.func_cancel)

    def erro_binning(self, binning_var):
        try:
            binning_filter = int(binning_var)
        except:
            binning_filter = 0
        return binning_filter

    def button_ok_func(self):
        try:
            self.var_save_ini_filters.set_filters_settings(self.setField_label_filter1.text(),
                                                           self.setField_wavelength_filter1.text(),
                                                           self.setField_exposure_filter1.text(),
                                                           self.setField_binning_filter1.currentIndex(),
                                                           self.setField_ccdgain_filter1.text(),
                                                           self.setField_label_filter2.text(),
                                                           self.setField_wavelength_filter2.text(),
                                                           self.setField_exposure_filter2.text(),
                                                           self.setField_binning_filter2.currentIndex(),
                                                           self.setField_ccdgain_filter2.text(),
                                                           self.setField_label_filter3.text(),
                                                           self.setField_wavelength_filter3.text(),
                                                           self.setField_exposure_filter3.text(),
                                                           self.setField_binning_filter3.currentIndex(),
                                                           self.setField_ccdgain_filter3.text(),
                                                           self.setField_label_filter4.text(),
                                                           self.setField_wavelength_filter4.text(),
                                                           self.setField_exposure_filter4.text(),
                                                           self.setField_binning_filter4.currentIndex(),
                                                           self.setField_ccdgain_filter4.text(),
                                                           self.setField_label_filter5.text(),
                                                           self.setField_wavelength_filter5.text(),
                                                           self.setField_exposure_filter5.text(),
                                                           self.setField_binning_filter5.currentIndex(),
                                                           self.setField_ccdgain_filter5.text(),
                                                           self.setField_label_filter6.text(),
                                                           self.setField_wavelength_filter6.text(),
                                                           self.setField_exposure_filter6.text(),
                                                           self.setField_binning_filter6.currentIndex(),
                                                           self.setField_ccdgain_filter6.text())
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

        self.setField_ccdgain_filter1.clear()
        self.setField_ccdgain_filter2.clear()
        self.setField_ccdgain_filter3.clear()
        self.setField_ccdgain_filter4.clear()
        self.setField_ccdgain_filter5.clear()
        self.setField_ccdgain_filter6.clear()

    def func_cancel(self):
        self.f.close()
