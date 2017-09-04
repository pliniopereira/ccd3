import os
import time
from time import sleep
import sys
from PyQt5 import QtCore

from src.business.configuration.settingsCamera import SettingsCamera
from src.business.configuration.settingsImage import SettingsImage
from src.business.sequence_filters.SettingsSequenceFilters import SettingsSequenceFilters
from src.business.shooters import LabelFilters
from src.controller.commons.Locker import Locker
from src.utils.camera import SbigDriver
from src.utils.camera.Image_Path import set_path
from src.utils.camera.Image_Processing import save_png, set_header, save_tif
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

        self.img = None

        self.lock = Locker()
        self.info = []

        self.filter_split_label = None

        self.count_aux = 0

        self.roda_filtros = FilterControl()

    def get_wish_filters_settings(self):
        settings = SettingsSequenceFilters()
        info_wish_filters = settings.get_sequence_filters_settings()

        my_list = []
        available_filters = LabelFilters.get_filter_settings()
        available_filters_list = list(available_filters)

        for i, c in enumerate(info_wish_filters):
            if c in available_filters_list:
                my_list.append(c)

        return my_list

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
                self.filter_split_label = LabelFilters.get_filter_settings()
            except Exception as e:
                print("get_filter_settings() -> {}".format(e))

        except Exception as e:
            print("Try ini definitive -> {}".format(e))

    def run(self):
        self.set_config_take_image()
        # print("\n\n\n")
        # print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        # print(str(self.filter_split_label))
        # print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        # print("\n\n\n")

        my_list = self.get_wish_filters_settings()

        try:
            if self.count_aux < len(my_list):
                index_of_dic = str(my_list[self.count_aux])
                aux = self.filter_split_label[str(index_of_dic)][0]
                # print("\n\n\n")
                # print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
                # print(index_of_dic)
                # print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
                # print("\n\n\n")
                # print("\n\n\n")
                # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                # print(str(self.filter_split_label))
                # print(str(self.count_aux))
                # print(str(my_list[self.count_aux]))
                # print(aux)
                # print(type(aux))
                # print(aux[0])
                # print(index_of_dic)
                # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                # print("\n\n\n")
                # print("\n\n")
                # print("---------------------------------------->")
                # # print(len(self.filter_split_label))
                # aux = list(aux)
                # print(aux)
                # print(aux[0])
                # print(aux[2])
                # print(aux[3])
                # print(aux[4])
                # print("---------------------------------------->")
                # print("\n\n")

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

                # print("\n\n")
                # print("---------------------------------------->")
                # print(str(self.count_aux))
                # print(len(my_list))
                # print("---------------------------------------->")
                #
                # print(aux)
                # print(aux[0])
                # print(aux[2])
                # print(aux[3])
                # print(aux[4])
                # print("\n\n")

            else:
                self.count_aux = 1
                index_of_dic = str(my_list[self.count_aux])
                aux = self.filter_split_label[str(index_of_dic)][0]

                print("\n\n")
                print("---------------------------------------->")
                print(str(self.count_aux))
                print("---------------------------------------->")

                print(aux)
                print(aux[0])
                print(aux[2])
                print(aux[3])
                print(aux[4])
                print("\n\n")

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

        '''
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
        '''

        try:
                # self.info = SbigDriver.photoshoot(self.exposure_time, self.prefix, self.binning, self.dark_photo,
                #                                   self.get_level1, self.get_level2, self.get_axis_xi,
                # self.get_axis_xf,
                #                                   self.get_axis_yi, self.get_axis_yf,
                #                                   self.get_ignore_crop,
                #                                   self.get_image_tif, self.get_image_fit)
                self.set_config_take_image()
                self.lock.set_acquire()
                self.img = SbigDriver.photoshoot(self.exposure_time, self.binning, self.dark_photo)
                print("\n\n")
                print(str(self.img))
                print(str(type(self.img)))
                print(sys.getsizeof(self.img))
                print(self.img.shape)
                print("\n\n")

                path, tempo = set_path()

                if not os.path.isdir(path):
                    os.makedirs(path)

                png_name = path + str(self.prefix) + "_" + str(tempo)
                tif_name = path + str(self.prefix) + "_" + str(tempo) + ".tif"
                fit_name = path + str(self.prefix) + "_" + str(tempo) + ".fit"
                # set_header(self.img)
                img_to_tif = self.img
                img_to_png = self.img
                img_to_fit = self.img

                save_tif(img_to_tif, tif_name)
                save_png(img_to_png, png_name)
                set_header(img_to_fit, fit_name)

                self.info = png_name
                self.init_image()
        except Exception as e:
            print("run SbigDriver.photoshoot ERROR -> {}".format(e))
        finally:
            self.lock.set_release()

    def init_image(self):
        try:
            # for i in self.info:
            #     print(i)

            self.img = Image(self.info[0], self.info[1], self.info[2], self.info[3], self.info[4], self.info[5])
        except Exception as e:
            print("Image('', '', '', '', '') -> {}".format(e))
            self.img = Image('', '', '', '', '')
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
            self.set_config_take_image()
            self.lock.set_acquire()
            self.img = SbigDriver.photoshoot(self.exposure_time, self.binning, self.dark_photo)

            path, tempo = set_path()

            if not os.path.isdir(path):
                os.makedirs(path)

            png_name = path + str(self.prefix) + str(tempo)
            set_header(self.img)
            save_png(self.img, png_name)
            self.init_image()
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)
            self.lock.set_release()
