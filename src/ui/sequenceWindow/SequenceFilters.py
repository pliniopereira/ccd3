from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QPushButton, QMessageBox

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
        self.obs_msg = None

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

        self.setWindowTitle("Acquisition Schedule")

        self.setting_values()

    def get_sequence_filters_settings(self):
        settings = SettingsSequenceFilters()
        info = settings.get_sequence_filters_settings()
        return info

    def create_filtros_disponiveis_group(self):
        group_box = QGroupBox("&Available Filters:")

        self.filters_disp = QtWidgets.QLabel(str(self.available_filters_and_exposure_time()))
        self.filters_disp.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignVCenter)

        group_box.setLayout(set_lvbox(set_hbox(self.filters_disp)))

        return group_box

    def create_wish_filters_group(self):
        group_box = QGroupBox("&Filter Sequence:")

        self.wish_sequence_filters_l = QtWidgets.QLineEdit(self)
        self.wish_sequence_filters_l.setMinimumWidth(250)

        available_filters_list_and_commons = LabelFilters.get_filter_settings()
        available_filters_list_and_commons = list(available_filters_list_and_commons)
        available_filters_list_and_commons.append(',')

        permited_filters = ''
        for x in available_filters_list_and_commons:
            permited_filters += ' ' + str(x)
        self.obs_msg = QtWidgets.QLabel("Only %s are allowed allowed" % permited_filters)
        self.obs_msg.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignVCenter)

        group_box.setLayout(set_lvbox(set_hbox(self.wish_sequence_filters_l),
                                      set_hbox(self.obs_msg)))

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
            available_filters_list_and_commons = LabelFilters.get_filter_settings()
            available_filters_list_and_commons = list(available_filters_list_and_commons)
            available_filters_list_and_commons.append(',')
            available_filters_list_and_commons.append(' ')


            # Percorre a string que está na box e testa caracter por caracter, permitindo somente numeros de filtors
            # disponiveis e ','.
            for x in self.wish_sequence_filters_l.text():
                if x not in available_filters_list_and_commons:
                    list_save_ok = False
                    break
                else:
                    list_save_ok = True
            if list_save_ok:
                self.sequencia_filtros.set_sequence_filters_settings(self.wish_sequence_filters_l.text())
                self.sequencia_filtros.save_settings()
                self.console.raise_text("Sequence Filters %s successfully saved!" % self.wish_sequence_filters_l.text(),
                                        1)
            else:
                print("Sequence Filters settings were not saved")
                self.console.raise_text("Sequence Filters settings were not saved.", 3)
                error_msg = ''
                for x in available_filters_list_and_commons:
                    error_msg += ' ' + str(x)
                QMessageBox.question(self, 'Error message',
                                     "Only %s are allowed!" % error_msg, QMessageBox.Ok)
        except Exception as e:
            print("Sequence Filters settings were not saved -> {}".format(e))
            self.console.raise_text("Sequence Filters settings were not saved.", 3)

    def func_cancel(self):
        self.seq_filtros_parent.close()

    def setting_values(self):
        info = self.get_sequence_filters_settings()
        self.set_values(info)

    def get_values(self):
        return self.wish_sequence_filters.text()

    def set_values(self, wish_sequence_filters):
        self.wish_sequence_filters_l.setText(wish_sequence_filters)

    def available_filters_and_exposure_time(self):
        try:
            filter_split_label = LabelFilters.get_filter_settings()

        except Exception as e:
            print("get_filter_settings() -> {}".format(e))

        show_filters = ''
        for filter_position_number in filter_split_label:

            filter_name = filter_split_label[filter_position_number][0]

            filter_position_number = str(filter_position_number)
            filter_name_str = str(filter_name[0])
            exposure_time_str = str(filter_name[2])

            show_filters += str(filter_position_number) + ":  Filter - " + filter_name_str[:3]

            if len(filter_name_str) == 1:
                show_filters += "    Exposure Time(s): " + exposure_time_str + "\n"
            elif len(filter_name_str) == 2:
                show_filters += "    Exposure Time(s): " + exposure_time_str + "\n"
            else:
                show_filters += "  Exposure Time(s): " + exposure_time_str + "\n"

        return show_filters
