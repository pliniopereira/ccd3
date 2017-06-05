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
        self.prefix = None
        self.exposure_time = None
        self.binning = None
        self.dark_photo = None

        self.get_level1 = None
        self.get_level2 = None
        self.get_axis_xi = None
        self.get_axis_xf = None
        self.get_axis_yi = None
        self.get_axis_yf = None
        self.get_ignore_crop = None

        self.get_image_tif = None
        self.get_image_fit = None

        self.img = None

        self.lock = Locker()
        self.info = []

        self.filter_split_l = None

        self.count_aux = 5

    def get_image_settings(self):
        """
        Pega os valores no ini image
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

        return info_image

    def get_camera_settings(self):
        """
        Pega os valores no ini camera
        info_cam[0] = temperature_camera
        info_cam[1] = tempo de espera até atingir temperatura desejada
        info_cam[2] = dark(Open or close shutter)
        """
        settings = SettingsCamera()
        info_cam = settings.get_camera_settings()

        return info_cam

    def get_filter_settings(self):
        """
        Pega os valores no ini filters
        info_filters[0] = label_field_1
        info_filters[1] = wavelength_field_1
        info_filters[2] = exposure_field_1
        info_filters[3] = binning_field_1
        info_filters[5] = label_field_2
        info_filters[6] = wavelength_field_2
        info_filters[7] = exposure_field_2
        info_filters[8] = binning_field_2
        info_filters[10] = label_field_3
        info_filters[11] = wavelength_field_3
        info_filters[12] = exposure_field_3
        info_filters[13] = binning_field_3
        info_filters[15] = label_field_4
        info_filters[16] = wavelength_field_4
        info_filters[17] = exposure_field_4
        info_filters[18] = binning_field_4
        info_filters[20] = label_field_5
        info_filters[21] = wavelength_field_5
        info_filters[22] = exposure_field_5
        info_filters[23] = binning_field_5
        info_filters[25] = label_field_6
        info_filters[26] = wavelength_field_6
        info_filters[27] = exposure_field_6
        info_filters[28] = binning_field_6
        """

        settings = SettingsFilters()
        info_filters_l = settings.get_filters_settings()

        n = 6
        self.filter_split_l = []
        len_l = len(info_filters_l)

        for i in range(n):
            start = int(i * len_l / n)
            end = int((i + 1) * len_l / n)
            self.filter_split_l.append(info_filters_l[start:end])

    def take_dark(self):
        """
        Manda instrução para o SbigDriver para tirar uma foto dark(shooter fechado)\
        com os valores na info[]
        """
        try:
            self.set_config_take_image()
            self.lock.set_acquire()
            self.info = SbigDriver.photoshoot(self.exposure_time, self.prefix, self.binning, 1,
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

    def set_config_take_image(self):
        """
        seta as configuracoes para se tirar uma foto
        """
        try:
            # try:
            #     print("\n\n")
            #     print("self.exposure_time " + str(self.exposure_time) + " " + str(type(self.exposure_time)))
            #     print("self.pre " + str(self.prefix) + " " + str(type(self.prefix)))
            #     print("self.binning " + str(self.binning) + " " + str(type(self.binning)))
            #     print("self.dark_photo " + str(self.dark_photo) + " " + str(type(self.dark_photo)))
            #     print("self.get_level1 " + str(self.get_level1) + " " + str(type(self.get_level1)))
            #     print("self.get_level2 " + str(self.get_level2) + " " + str(type(self.get_level2)))
            #     print("self.get_axis_xi " + str(self.get_axis_xi) + " " + str(type(self.get_axis_xi)))
            #     print("self.get_axis_xf " + str(self.get_axis_xf) + " " + str(type(self.get_axis_xf)))
            #     print("self.get_axis_yi " + str(self.get_axis_yi) + " " + str(type(self.get_axis_yi)))
            #     print("self.get_axis_yf " + str(self.get_axis_yf) + " " + str(type(self.get_axis_yf)))
            #     print("self.get_ignore_crop " + str(self.get_ignore_crop) + " " + str(type(self.get_ignore_crop)))
            #     print("self.get_image_tif " + str(self.get_image_tif) + " " + str(type(self.get_image_tif)))
            #     print("self.get_image_fit " + str(self.get_image_fit) + " " + str(type(self.get_image_fit)))
            #     print("\n\n")
            # except Exception as e:
            #     print("Try ini 1 -> {}".format(e))

            info_cam = self.get_camera_settings()
            info_image = self.get_image_settings()

            try:
                self.dark_photo = int(info_cam[2])
            except Exception as e:
                print("self.dark_photo = 0 -> {}".format(e))
                self.dark_photo = 0

            try:
                self.get_level1 = float(info_image[0])
            except Exception as e:
                print("self.get_level1 = 0.1 -> {}".format(e))
                self.get_level1 = 0.1

            try:
                self.get_level2 = float(info_image[1])
            except Exception as e:
                print("self.get_level2 = 0.99 -> {}".format(e))
                self.get_level2 = 0.99

            try:
                self.get_axis_xi = float(info_image[2])
            except Exception as e:
                print("self.get_axis_xi = 0 -> {}".format(e))
                self.get_axis_xi = 0

            try:
                self.get_axis_xf = float(info_image[3])
            except Exception as e:
                print("self.get_axis_xf = 0 -> {}".format(e))
                self.get_axis_xf = 0

            try:
                self.get_axis_yi = float(info_image[4])
            except Exception as e:
                print("self.get_axis_yi = 0 -> {}".format(e))
                self.get_axis_yi = 0

            try:
                self.get_axis_yf = float(info_image[5])
            except Exception as e:
                print("self.get_axis_yf = 0 -> {}".format(e))
                self.get_axis_yf = 0

            try:
                self.get_ignore_crop = info_image[6]
            except Exception as e:
                print("self.get_ignore_crop = True -> {}".format(e))
                self.get_ignore_crop = True

            try:
                self.get_image_tif = info_image[7]
            except Exception as e:
                print("self.get_image_tif = True -> {}".format(e))
                self.get_image_fit = True
            try:
                self.get_image_fit = info_image[8]
            except Exception as e:
                print("self.get_image_fit = True -> {}".format(e))
                self.get_image_fit = True
            try:
                self.get_filter_settings()
            except Exception as e:
                print("get_filter_settings() -> {}".format(e))

        except Exception as e:
            print("Try ini definitive -> {}".format(e))

    def run(self):
        self.set_config_take_image()

        try:
            aux = self.filter_split_l[self.count_aux]
            print(aux)
            print(aux[0])
            print(aux[2])
            print(aux[3])

            self.prefix = aux[0]
            self.exposure_time = aux[2]
            self.binning = aux[3]
        except Exception as e:
            print("Try filter ini -> {}".format(e))
        self.lock.set_acquire()

        print("\n\n")
        print("self.exposure_time " + str(self.exposure_time) + " " + str(type(self.exposure_time)))
        print("self.pre " + str(self.prefix) + " " + str(type(self.prefix)))
        print("self.binning " + str(self.binning) + " " + str(type(self.binning)))
        print("self.dark_photo " + str(self.dark_photo) + " " + str(type(self.dark_photo)))
        print("self.get_level1 " + str(self.get_level1) + " " + str(type(self.get_level1)))
        print("self.get_level2 " + str(self.get_level2) + " " + str(type(self.get_level2)))
        print("self.get_axis_xi " + str(self.get_axis_xi) + " " + str(type(self.get_axis_xi)))
        print("self.get_axis_xf " + str(self.get_axis_xf) + " " + str(type(self.get_axis_xf)))
        print("self.get_axis_yi " + str(self.get_axis_yi) + " " + str(type(self.get_axis_yi)))
        print("self.get_axis_yf " + str(self.get_axis_yf) + " " + str(type(self.get_axis_yf)))
        print("self.get_ignore_crop " + str(self.get_ignore_crop) + " " + str(type(self.get_ignore_crop)))
        print("self.get_image_tif " + str(self.get_image_tif) + " " + str(type(self.get_image_tif)))
        print("self.get_image_fit " + str(self.get_image_fit) + " " + str(type(self.get_image_fit)))
        print("\n\n")

        try:
                self.info = SbigDriver.photoshoot(self.exposure_time, self.prefix, self.binning, self.dark_photo,
                                                  self.get_level1, self.get_level2, self.get_axis_xi, self.get_axis_xf,
                                                  self.get_axis_yi, self.get_axis_yf,
                                                  self.get_ignore_crop,
                                                  self.get_image_tif, self.get_image_fit)
                self.init_image()
        except Exception as e:
            print("run SbigDriver.photoshoot ERROR -> {}".format(e))
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
