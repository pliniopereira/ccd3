from PyQt5 import QtCore

from src.business.filters.constants import filters as f


class SettingsFilters:
    def __init__(self):
        self._settings = QtCore.QSettings()
        self.setup_settings()

    def setup_settings(self):
        self._settings = QtCore.QSettings(f.FILTERSFILE, QtCore.QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

    def save_settings(self):
        self._settings.sync()

    def set_filters_settings(self, x):
        self._settings.setValue(f.X, x)

    def get_filters_settings(self):
        return self._settings.value(f.X)

    def get_filepath(self):
        return self._settings.value(f.FILTERSFILE)
