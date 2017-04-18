from PyQt5 import QtCore

from src.business.configuration.constants import imager as i


class SettingsImager:
    def __init__(self):
        self._settings = QtCore.QSettings()
        self.setup_settings()

    def setup_settings(self):
        self._settings = QtCore.QSettings(i.FILENAME, QtCore.QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

    def save_settings(self):
        self._settings.sync()

    def set_imager_settings(self, temperature_camera, time_cooling, dark_photo):
        self._settings.setValue(i.TEMPERATURE, temperature_camera)
        self._settings.setValue(i.TIMECOOLING, time_cooling)
        self._settings.setValue(i.DARK_PHOTO, dark_photo)

    def get_imager_settings(self):
        return self._settings.value(i.TEMPERATURE),\
               self._settings.value(i.TIMECOOLING),\
               self._settings.value(i.DARK_PHOTO)

    def get_filepath(self):
        return self._settings.value(i.FILENAME)
