from PyQt5 import QtCore

from src.business.filters.constants import filters as f


class SettingsFilters:
    def __init__(self):
        self._settings = QtCore.QSettings()
        self.setup_settings()

    def setup_settings(self):
        self._settings = QtCore.QSettings(f.FILENAME, QtCore.QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

    def save_settings(self):
        self._settings.sync()

    def set_filters_settings(self, temperature_camera, pre, exp, bin, time, time_cooling, get_level1,\
                            get_level2, dark_photo, crop_xi, crop_xf, crop_yi, crop_yf, ignore_crop):
        """
        :param temperature_camera: seta o valor que a camera deve atingir para começo das observacoes
        :param pre: prefixo, dá nome ao path que vai ser criado no comeco das observacoes\
        e onde as imagens ficaram salvas
        :param exp: Tempo de exposição.
        :param bin: valor agrupamento de nxn pixeis para 1x1 pixel.
        :param time: Intervalo de tempo entre as fotos.
        :param time_cooling: tempo que a camera espera atingir a temperatura seta no campo \
        temperature_camera, caso nao seja atingida a observacao se inicia indepedente da \
        temperatura alcancada ou nao
        :param get_level1:  nível inferior normalizado para ajuste de contraste
        :param get_level2: nível superior normalizado para ajuste de contraste
        :param dark_photo: valor guardado que defini se a foto tirada terá o shooter fechada \
        ou aberta.
        :param crop_xi:
        :param crop_xf:
        :param crop_yi:
        :param crop_yf:
        :param ignore_crop:
        :return:
        """
        self._settings.setValue(f.TEMPERATURE, temperature_camera)
        self._settings.setValue(f.PREFIXO, pre)
        self._settings.setValue(f.EXPOSICAO, exp)
        self._settings.setValue(f.BINNING, bin)
        self._settings.setValue(f.TIMEPHOTO, time)
        self._settings.setValue(f.TIMECOOLING, time_cooling)
        self._settings.setValue(f.GET_LEVEL1, get_level1)
        self._settings.setValue(f.GET_LEVEL2, get_level2)
        self._settings.setValue(f.DARK_PHOTO, dark_photo)
        self._settings.setValue(f.CROP_X_AXIS_XI, crop_xi)
        self._settings.setValue(f.CROP_X_AXIS_XF, crop_xf)
        self._settings.setValue(f.CROP_Y_AXIS_YI, crop_yi)
        self._settings.setValue(f.CROP_Y_AXIS_YF, crop_yf)
        self._settings.setValue(f.CHEBOX_IGNORE_CROP, ignore_crop)

    def get_filters_settings(self):
        return self._settings.value(f.TEMPERATURE), self._settings.value(f.PREFIXO), self._settings.value(f.EXPOSICAO),\
               self._settings.value(f.BINNING), self._settings.value(f.TIMEPHOTO), self._settings.value(f.TIMECOOLING),\
               self._settings.value(f.GET_LEVEL1), self._settings.value(f.GET_LEVEL2), self._settings.value(f.DARK_PHOTO),\
               self._settings.value(f.CROP_X_AXIS_XI), self._settings.value(f.CROP_X_AXIS_XF),\
               self._settings.value(f.CROP_Y_AXIS_YI), self._settings.value(f.CROP_Y_AXIS_YF),\
               self._settings.value(f.CHEBOX_IGNORE_CROP, True, type=bool)

    def get_filepath(self):
        return self._settings.value(f.FILENAME)
