from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QPushButton

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.sequence_filters.SettingsSequenceFilters import SettingsSequenceFilters
from src.business.shooters import LabelFilters
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
        self.showfiltersl = None

        # Instance attributes create_push_button_group
        self.saveButton = None
        self.cancelButton = None
        self.clearButton = None

        self.sequencia_filtros = SettingsSequenceFilters()

        self.filters_disp_var = None

        self.console = ConsoleThreadOutput()

        self.count_aux = 0

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
        group_box = QGroupBox("&Filters Available:")

        self.filters_disp = QtWidgets.QLabel(str(self.available_filters()))
        self.filters_disp.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignVCenter)

        group_box.setLayout(set_lvbox(set_hbox(self.filters_disp)))

        return group_box

    def create_wish_filters_group(self):
        group_box = QGroupBox("&Wish Filters")

        self.wish_sequence_filters_l = QtWidgets.QLineEdit(self)
        self.wish_sequence_filters_l.setMinimumWidth(250)

        group_box.setLayout(set_lvbox(set_hbox(self.wish_sequence_filters_l)))

        return group_box

    def create_push_button_group(self):
        group_box = QGroupBox()
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.button_ok_func)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.func_cancel)

        group_box.setLayout(set_lvbox(set_hbox(self.saveButton, self.cancelButton)))

        return group_box

    def button_ok_func(self):
        try:
            self.sequencia_filtros.set_sequence_filters_settings(self.wish_sequence_filters_l.text())
            self.sequencia_filtros.save_settings()
            self.console.raise_text("Sequence Filters settings successfully saved!", 1)

        except Exception as e:
            print("Sequence Filters settings were not saved -> {}".format(e))
            self.console.raise_text("Sequence Filters settings were not saved.", 3)

    def func_cancel(self):
        self.seq_filtros_parent.close()

    def setting_values(self):
        info = self.get_sequence_filters_settings()
        self.set_values(info[0])

    def get_values(self):
        return self.wish_sequence_filters_l.text()

    def set_values(self, wish_sequence_filters_l):
        self.wish_sequence_filters_l.setText(wish_sequence_filters_l)

    def available_filters(self):
        try:
            filter_split_label = LabelFilters.get_filter_settings()
        except Exception as e:
            print("get_filter_settings() -> {}".format(e))

        show_filters = ''
        for x in filter_split_label:
            filter_name = filter_split_label[x][0]
            show_filters += x + ": Filter - " + str(filter_name[0]) + "\n"

        return show_filters
