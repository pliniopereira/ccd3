import time

from PyQt5 import QtCore

from src.business.configuration.settingsCamera import SettingsCamera
from src.business.configuration.settingsImage import SettingsImage
from src.business.filters.settingsFilters import SettingsFilters
from src.business.models.image import Image
from src.controller.commons.Locker import Locker
from src.utils.camera import SbigDriver


class SThread(QtCore.QThread):
    """
    Threads são fluxos de programas que executam em paralelo dentro de uma aplicação, isto é,\
    uma ramificação de uma parte da aplicação que é executada de forma independente e\
    escalonada independentemente do fluxo inicial da aplicação.
    Fonte: http://imasters.com.br/artigo/20127/py/threads-em-python/?trace=1519021197&source=single
    """
    def __init__(self):
        super(SThread, self).__init__()
        self.lock = Locker()
        self.info = []
        self.img = None
        self.generic_count = 0

    @staticmethod
    def get_image_settings():
        """
        pega os valores no ini imager
        info_image[0] = get_level1
        info_image[1] = get_level2
        info_image[2] = crop_xi
        info_image[3] = crop_xf
        info_image[4] = crop_yi
        info_image[5] = crop_yf
        info_image[6] = ignore_crop
        info_image[7] = image_tif
        info_image[8] = image_fit
        """

        settings = SettingsImage()
        info_image = settings.get_image_settings()
        print(info_image)

        return info_image

    @staticmethod
    def get_camera_settings():
        """
        pega os valores no ini camera
        info_cam[0] = temperature_camera
        info_cam[1] = tempo de espera até atingir temperatura desejada
        info_cam[2] = dark(Open or close shutter)
        """
        settings = SettingsCamera()
        info_cam = settings.get_camera_settings()

        return info_cam

    @staticmethod
    def get_filter_settings():
        """
        pega os valores no ini filters
        info_filters[0] = label_field_1
        info_filters[1] = wavelength_field_1
        info_filters[2] = exposure_field_1
        info_filters[3] = binning_field_1
        info_filters[4] = ccd_gain_field_1
        info_filters[5] = label_field_2
        info_filters[6] = wavelength_field_2
        info_filters[7] = exposure_field_2
        info_filters[8] = binning_field_2
        info_filters[9] = ccd_gain_field_2
        info_filters[10] = label_field_3
        info_filters[11] = wavelength_field_3
        info_filters[12] = exposure_field_3
        info_filters[13] = binning_field_3
        info_filters[14] = ccd_gain_field_3
        info_filters[15] = label_field_4
        info_filters[16] = wavelength_field_4
        info_filters[17] = exposure_field_4
        info_filters[18] = binning_field_4
        info_filters[19] = ccd_gain_field_4
        info_filters[20] = label_field_5
        info_filters[21] = wavelength_field_5
        info_filters[22] = exposure_field_5
        info_filters[23] = binning_field_5
        info_filters[24] = ccd_gain_field_5
        info_filters[25] = label_field_6
        info_filters[26] = wavelength_field_6
        info_filters[27] = exposure_field_6
        info_filters[28] = binning_field_6
        info_filters[29] = ccd_gain_field_6
        """

        settings = SettingsFilters()
        info_filters = settings.get_filters_settings()

        print(info_filters)

        return info_filters

    def take_dark(self):
        """
        Manda instrução para o SbigDriver para tirar uma foto dark(shooter fechado)\
        com os valores na info[]
        """
        try:
            self.set_etime_pre_binning()
            self.lock.set_acquire()
            self.info = SbigDriver.photoshoot(self.etime, self.pre, self.b, 1,
                                              self.get_level1, self.get_level2,
                                              self.get_axis_xi, self.get_axis_xf,
                                              self.get_axis_yi, self.get_axis_yf,
                                              self.get_ignore_crop,
                                              self.get_image_tif,
                                              self.get_image_fit)
            self.init_image()
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)
            self.lock.set_release()

    def set_etime_pre_binning(self):
        """
        seta os valores para o tempo de exposição = etime, prefixo, binning, se a foto é dark ou não,\
        e valores Image contrast: bottom e top level
        """

        try:
            info = self.get_camera_settings()

            self.pre = str(info[1])

            self.etime = float(info[2])
            if self.etime <= 0.12:
                self.etime = 0.12 * 100
            elif self.etime >= 3600:
                 self.etime = 3600 * 100
            else:
                self.etime = float(info[2]) * 100
            self.etime = int(self.etime)

            self.b = int(info[3])

            self.get_level1 = float(info[6])
            self.get_level2 = float(info[7])

            self.dark_photo = int(info[8])

            self.get_axis_xi = int(info[9])
            self.get_axis_xf = int(info[10])
            self.get_axis_yi = int(info[11])
            self.get_axis_yf = int(info[12])

            self.get_ignore_crop = info[13]

            self.get_image_tif = info[14]
            self.get_image_fit = info[15]

        except Exception as e:
            print(e)
            self.etime = 100
            self.b = 0
            self.dark_photo = 1
            self.get_level1 = 0.1
            self.get_level2 = 0.99

            if str(info[1]) != '':
                self.pre = str(info[1])
            else:
                self.pre = 'pre'

            self.get_axis_xi = info[9]
            self.get_axis_xf = info[10]
            self.get_axis_yi = info[11]
            self.get_axis_yf = info[12]

            self.get_ignore_crop = True

            self.get_image_tif = True
            self.get_image_fit = True

    def run(self):
        self.set_etime_pre_binning()
        self.lock.set_acquire()
        try:
            self.info = SbigDriver.photoshoot(self.etime, self.pre, self.b, self.dark_photo, self.get_level1,
                                              self.get_level2, self.get_axis_xi, self.get_axis_xf, self.get_axis_yi,
                                              self.get_axis_yf, self.get_ignore_crop,
                                              self.get_image_tif, self.get_image_fit)
            self.init_image()
        except Exception as e:
            print(e)
        finally:
            self.lock.set_release()

    def init_image(self):
        try:
            for i in self.info:
                print(i)

            self.img = Image(self.info[0], self.info[1], self.info[2], self.info[3], self.info[4])
        except Exception as e:
            print("Image('', '', '', '', '') -> {}".format(e))
            self.img = Image('', '', '', '', '')
        return self.img

    def get_image_info(self):
        return self.img
