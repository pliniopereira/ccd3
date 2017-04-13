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

        self.setLayout(set_lvbox(set_hbox(self.setField_x_label, self.setField_x),
                                 set_hbox(self.buttonok, self.button_clear, self.buttoncancel, stretch2=1)))

    def get_values(self):
        return self.var_save_ini_filters.SettingsFilters()

    def setting_values(self):
        info = self.get_values()
        self.set_values(info[0])

    def set_values(self, x):
        self.setField_x.setText(x)

    def create_filters_widgets(self):
        self.setField_x_label = QtWidgets.QLabel("X", self)
        self.setField_x_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.setField_x = QtWidgets.QLineEdit(self)
        self.setField_x.setMaximumWidth(100)

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
        self.setField_x.clear()

    def func_cancel(self):
        self.f.close()
