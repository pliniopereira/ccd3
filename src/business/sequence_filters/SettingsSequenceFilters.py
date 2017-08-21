from PyQt5 import QtCore

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.sequence_filters.constants import sequence as s


class SettingsSequenceFilters:
    def __init__(self):
        self._settings = QtCore.QSettings()
        self.setup_settings()
        self.console = ConsoleThreadOutput()

    def setup_settings(self):
        self._settings = QtCore.QSettings(s.SEQUENCE_FILTERS, QtCore.QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

    def save_settings(self):
        self._settings.sync()

    def set_sequence_filters_settings(self, showfilters, ignore_filters_wish, wish_sequence_filters):
        self._settings.setValue(s.SHOWFILTERS, showfilters)
        self._settings.setValue(s.IGNORE_FILTERS_WISH, ignore_filters_wish)
        self._settings.setValue(s.WISH_SEQUENCE_FILTERS, wish_sequence_filters)

    def get_sequence_filters_settings(self):
        return self._settings.value(s.SHOWFILTERS), \
               self._settings.value(s.IGNORE_FILTERS_WISH, True, type=bool), \
               self._settings.value(s.WISH_SEQUENCE_FILTERS)


def get_filepath(self):
    return self._settings.value(s.SEQUENCE_FILTERS)
