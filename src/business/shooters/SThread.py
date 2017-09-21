import os
import time
from time import sleep

from PyQt5 import QtCore

from src.business.models.image import Image
from src.business.shooters.InfosForSThread import get_wish_filters_settings, get_camera_settings, get_image_settings, \
    get_project_settings, get_filter_settings
# from src.controller.Camera import Camera
from src.controller.commons.Locker import Locker
from src.utils.camera import SbigDriver
from src.utils.camera.Image_Path import set_path
from src.utils.camera.Image_Processing import save_png, save_tif, save_fit, get_date_hour
from src.utils.rodafiltros.FilterControl import FilterControl


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
        self.get_image_png = None

        self.temperatura = None

        self.img = None

        self.for_headers_list = []

        self.lock = Locker()
        self.info = []

        self.filter_split_label = None

        self.count_aux = 0

        self.roda_filtros = FilterControl()

    def set_config_take_image(self):
        """
        seta as configuracoes para se tirar uma foto
        """
        try:
            info_cam = get_camera_settings()
            self.for_headers_list.append(info_cam)

            info_image = get_image_settings()

            try:
                self.dark_photo = int(info_cam[2])
            except Exception as e:
                print("self.dark_photo = 0 -> {}".format(e))
                self.dark_photo = 0

            try:
                self.get_level1 = float(info_image[0])
            except Exception as e:
                # print("self.get_level1 = 0.1 -> {}".format(e))
                self.get_level1 = 0.1

            try:
                self.get_level2 = float(info_image[1])
            except Exception as e:
                # print("self.get_level2 = 0.99 -> {}".format(e))
                self.get_level2 = 0.99

            try:
                self.get_axis_xi = float(info_image[2])
            except Exception as e:
                # print("self.get_axis_xi = 0 -> {}".format(e))
                self.get_axis_xi = 0

            try:
                self.get_axis_xf = float(info_image[3])
            except Exception as e:
                # print("self.get_axis_xf = 0 -> {}".format(e))
                self.get_axis_xf = 0

            try:
                self.get_axis_yi = float(info_image[4])
            except Exception as e:
                # print("self.get_axis_yi = 0 -> {}".format(e))
                self.get_axis_yi = 0

            try:
                self.get_axis_yf = float(info_image[5])
            except Exception as e:
                # print("self.get_axis_yf = 0 -> {}".format(e))
                self.get_axis_yf = 0

            try:
                self.get_ignore_crop = info_image[6]
            except Exception as e:
                print("self.get_ignore_crop = True -> {}".format(e))
                self.get_ignore_crop = True

            try:
                self.get_image_png = info_image[7]
            except Exception as e:
                print("self.get_image_png  = True -> {}".format(e))
                self.get_image_png  = True

            try:
                self.get_image_tif = info_image[8]
            except Exception as e:
                print("self.get_image_tif = True -> {}".format(e))
                self.get_image_fit = True
            try:
                self.get_image_fit = info_image[9]
            except Exception as e:
                print("self.get_image_fit = True -> {}".format(e))
                self.get_image_fit = True
            try:
                self.filter_split_label = get_filter_settings()

            except Exception as e:
                print("get_filter_settings() -> {}".format(e))

        except Exception as e:
            print("Try ini definitive -> {}".format(e))

    def run(self):
        self.set_config_take_image()
        self.lock.set_acquire()

        my_list = get_wish_filters_settings()  # list of schedule

        try:
            if self.count_aux < len(my_list):

                index_of_dic = str(my_list[self.count_aux])

                aux = self.filter_split_label[str(index_of_dic)][0]
                self.for_headers_list.append(aux)

                aux = list(aux)
                '''
                aux[0] = self.prefix
                aux[2] = self.exposure_time
                aux[3] = self.binning
                aux[4] = wish filter
                '''

                self.prefix = str(aux[0])

                self.exposure_time = float(aux[2])
                if self.exposure_time <= 0.12:
                    self.exposure_time = 0.12 * 100
                elif self.exposure_time >= 3600:
                    self.exposure_time = 3600 * 100
                else:
                    self.exposure_time = float(aux[2]) * 100
                self.exposure_time = int(self.exposure_time)

                self.binning = int(aux[3])

                self.count_aux += 1

                self.filter_wheel_control(int(aux[4]))

            else:
                self.count_aux = 1
                index_of_dic = str(my_list[self.count_aux])
                aux = self.filter_split_label[str(index_of_dic)][0]
                self.for_headers_list.append(aux)

                self.prefix = str(aux[0])
                self.exposure_time = float(aux[2])
                self.binning = int(aux[3])

                self.exposure_time = float(aux[2])
                if self.exposure_time <= 0.12:
                    self.exposure_time = 0.12 * 100
                elif self.exposure_time >= 3600:
                    self.exposure_time = 3600 * 100
                else:
                    self.exposure_time = float(aux[2]) * 100
                self.exposure_time = int(self.exposure_time)

                self.filter_wheel_control(aux[4])

                self.count_aux += 1

        except Exception as e:
            print("Try filter ini -> {}".format(e))

        self.for_headers_list.append(self.get_level1)
        self.for_headers_list.append(self.get_level2)
        self.for_headers_list.append(self.get_axis_xi)
        self.for_headers_list.append(self.get_axis_xf)
        self.for_headers_list.append(self.get_axis_yi)
        self.for_headers_list.append(self.get_axis_yf)
        self.for_headers_list.append(self.get_ignore_crop)

        project_infos = get_project_settings()

        name_observatory = project_infos[2][1]

        path, tempo = set_path()

        image_name = path + str(self.prefix) + "_" + str(name_observatory) + "_" + str(tempo)

        try:
            self.img = SbigDriver.photoshoot(self.exposure_time, self.binning, self.dark_photo)
        except Exception as e:
            print("self.img = SbigDriver.photoshoot ERROR -> " + str(e))

        if not os.path.isdir(path):
            os.makedirs(path)

        self.for_headers_list.append(tempo)
        self.for_headers_list.append(project_infos)
        try:
            self.temperatura = SbigDriver.get_temperature()
            self.temperatura = "{0:.2f}".format(float(self.temperatura[3]))
            self.for_headers_list.append(self.temperatura)
        except Exception as e:
            print("Exception self.temperatura -> {}".format(e))

        if self.get_image_png:
            try:
                save_png(self.img, image_name, self.for_headers_list)
            except Exception as e:
                print("Exception save_png() -> {}".format(e))
        elif self.get_image_tif:
            try:
                save_tif(self.img, image_name)
            except Exception as e:
                print("Exception save_tif() -> {}".format(e))
        elif self.get_image_fit:
            try:
                save_fit(self.img, image_name, self.for_headers_list)
            except Exception as e:
                print("Exception save_fit() -> {}".format(e))
        else:
            try:
                save_png(self.img, image_name, self.for_headers_list)
            except Exception as e:
                print("Exception save_png() -> {}".format(e))

        try:
            data, hora = get_date_hour(tempo)
            self.info = path, self.img, data, hora
            self.init_image()
        except Exception as e:
            print("run init_image() -> {}".format(e))

        except Exception as e:
            print("run ERROR -> {}".format(e))
        finally:
            self.for_headers_list = []
            self.lock.set_release()

    def init_image(self):
        try:
            # for i in self.info:
            #     print(i)

            self.img = Image(self.info[0], self.info[1], self.info[2], self.info[3])
        except Exception as e:
            print("Image('', '', '', '') -> {}".format(e))
            self.img = Image('', '', '', '')
        return self.img

    def get_image_info(self):
        return self.img

    def filter_wheel_control(self, wish_filter_int):
        try:
            sleep(1)
            wish_filter_int = int(wish_filter_int)
            self.roda_filtros.filter_wheel_control(wish_filter_int)
            sleep(1)
        except Exception as e:
            self.roda_filtros.home_reset()
            print(e)

    def take_dark(self):
        """
        Manda instrução para o SbigDriver para tirar uma foto dark(shooter fechado)\
        com os valores na info[]
        """
        try:
            # self.info = SbigDriver.photoshoot(self.exposure_time, self.prefix, self.binning, self.dark_photo,
            #                                   self.get_level1, self.get_level2, self.get_axis_xi,
            # self.get_axis_xf,
            #                                   self.get_axis_yi, self.get_axis_yf,
            #                                   self.get_ignore_crop,
            #                                   self.get_image_tif, self.get_image_fit)
            self.set_config_take_image()
            self.lock.set_acquire()
            try:
                print("\n\n")
                print("self.exposure_time = " + str(self.exposure_time))
                print("self.binning = " + str(self.binning))
                print("self.dark_photo = " + str(self.dark_photo))
                print("\n\n")

                self.img = SbigDriver.photoshoot(self.exposure_time, self.binning, 1)
            except Exception as e:
                print(e)

            path, tempo = set_path()

            if not os.path.isdir(path):
                os.makedirs(path)

            image_name = path + str(self.prefix) + "_" + str(tempo)

            save_png(self.img, image_name)
            save_tif(self.img, image_name)
            try:
                save_fit(self.img, image_name)
            except Exception as e:
                print("Exception save_fit() -> {}".format(e))

            self.info = self.img
            try:
                self.init_image()
            except Exception as e:
                print("run init_image() -> {}".format(e))
        except Exception as e:
            print("run take_dark ERROR -> {}".format(e))
        finally:
            time.sleep(1)
            self.lock.set_release()
