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

    def set_camera_settings(self, temperature_camera, time_cooling, dark_photo):
        """
        :param temperature_camera: seta o valor que a camera deve atingir para começo das observacoes
        :param time_cooling: tempo que a camera espera atingir a temperatura seta no campo temperature_camera, caso nao
        seja atingida a observacao se inicia indepedente da temperatura alcancada ou nao
        :param dark_photo: valor guardado que defini se a foto tirada terá o shooter fechada ou aberta.
        """
        self._settings.setValue(c.TEMPERATURE, temperature_camera)
        self._settings.setValue(c.TIMECOOLING, time_cooling)
        self._settings.setValue(c.DARK_PHOTO, dark_photo)

    def get_camera_settings(self):
        return self._settings.value(c.TEMPERATURE), \
               self._settings.value(c.TIMECOOLING), \
               self._settings.value(c.DARK_PHOTO)

    def get_filepath(self):
        return self._settings.value(c.FILENAME)
