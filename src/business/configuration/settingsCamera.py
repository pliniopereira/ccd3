from PyQt5 import QtCore

from src.business.configuration.constants import camera as c


class SettingsCamera:
    def __init__(self):
        self._settings = QtCore.QSettings()
        self.setup_settings()

    def setup_settings(self):
        self._settings = QtCore.QSettings(c.FILENAME, QtCore.QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

    def save_settings(self):
        self._settings.sync()

    def set_camera_settings(self, temperature_camera, time_cooling):
        """
        :param temperature_camera: seta o valor que a camera deve atingir para começo das observacoes
        :param time_cooling: tempo que a camera espera atingir a temperatura seta no campo temperature_camera, caso nao
        seja atingida a observacao se inicia indepedente da temperatura alcancada ou nao
        """
        self._settings.setValue(c.TEMPERATURE, temperature_camera)
        self._settings.setValue(c.TIMECOOLING, time_cooling)

    def get_camera_settings(self):
        return self._settings.value(c.TEMPERATURE), \
               self._settings.value(c.TIMECOOLING)

    def get_filepath(self):
        return self._settings.value(c.FILENAME)
