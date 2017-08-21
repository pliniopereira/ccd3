from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QPushButton)

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.sequence_filters.SettingsSequenceFilters import SettingsSequenceFilters
from src.ui.commons.layout import set_lvbox, set_hbox


class SequenceFilters(QtWidgets.QWidget):
    # Cria os campos e espaços no menu filter sequence_filters window

    def __init__(self, parent=None):
        super(SequenceFilters, self).__init__(parent)
        # Instance attributes create_filtros_disponiveis_group
        self.filters_disp = None
        self.showfilters = None

        # Instance attributes create_wish_filters_group
        self.wish_sequence_filters_l = None
        self.ignore_filters_wish_l = None
        self.sequence_desejada = None

        # Instance attributes create_push_button_group
        self.saveButton = None
        self.cancelButton = None
        self.clearButton = None

        self.sequencia_filtros = SettingsSequenceFilters()

        self.console = ConsoleThreadOutput()

        self.seq_filtros_parent = parent

        grid = QGridLayout()
        grid.addWidget(self.create_filtros_disponiveis_group(), 2, 0)
        grid.addWidget(self.create_wish_filters_group(), 4, 0)
        grid.addWidget(self.create_push_button_group(), 5, 0)
        self.setLayout(grid)

        self.setWindowTitle("Sequence Filter Box")

        self.setting_values()

    def get_sequence_filters_settings(self):
        settings = SettingsSequenceFilters()
        info = settings.get_sequence_filters_settings()
        return info

    def create_filtros_disponiveis_group(self):
        group_box = QGroupBox("&Filters Disp:")
        group_box.setCheckable(True)
        group_box.setChecked(True)

        self.filters_disp = QtWidgets.QLabel("Filters Disp:", self)
        self.filters_disp.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.showfiltersl = QtWidgets.QLineEdit(self)
        self.showfiltersl.setMaximumWidth(50)
        self.showfiltersl.setValidator(QIntValidator(-100, 30))

        group_box.setLayout(set_lvbox(set_hbox(self.filters_disp, self.showfiltersl)))

        return group_box

    def create_wish_filters_group(self):
        group_box = QGroupBox("&Wish Filters")
        group_box.setCheckable(True)
        group_box.setChecked(False)

        self.ignore_filters_wish_l = QtWidgets.QCheckBox('Ignore Wish Filters', self)

        self.sequence_desejada = QtWidgets.QLabel("Sequencia Desejada", self)
        self.wish_sequence_filters_l = QtWidgets.QLineEdit(self)
        self.wish_sequence_filters_l.setMaximumWidth(50)

        group_box.setLayout(set_lvbox(set_hbox(self.ignore_filters_wish_l),
                                      set_hbox(self.sequence_desejada),
                                      set_hbox(self.wish_sequence_filters_l)))

        return group_box

    def create_push_button_group(self):
        group_box = QGroupBox()
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.button_ok_func)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.func_cancel)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clear_all)

        group_box.setLayout(set_lvbox(set_hbox(self.saveButton, self.clearButton, self.cancelButton)))

        return group_box

    def button_ok_func(self):
        try:
            self.sequencia_filtros.set_sequence_filters_settings(self.showfiltersl.text(),
                                                                 self.ignore_filters_wish_l.isChecked(),
                                                                 self.wish_sequence_filters_l.text())
            self.sequencia_filtros.save_settings()
            self.console.raise_text("Sequence Filters settings successfully saved!", 1)

        except Exception as e:
            print("Sequence Filters settings were not saved -> {}".format(e))
            self.console.raise_text("Sequence Filters settings were not saved.", 3)

    def clear_all(self):
        self.showfiltersl.clear()
        self.wish_sequence_filters_l.clear()

    def func_cancel(self):
        self.seq_filtros_parent.close()

    def setting_values(self):
        info = self.get_sequence_filters_settings()
        self.set_values(info[0], info[1], info[2])

    def set_values(self, showfilters, ignore_filters_wish, wish_sequence_filters_l):
        self.showfiltersl.setText(showfilters)
        self.ignore_filters_wish_l.setChecked(ignore_filters_wish)
        self.wish_sequence_filters_l.setText(wish_sequence_filters_l)
