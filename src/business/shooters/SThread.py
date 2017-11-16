import math
import os
from datetime import datetime
from time import sleep

import ephem
from PyQt5 import QtCore

from src.business.EphemObserverFactory import EphemObserverFactory
from src.business.models.image import Image
from src.business.shooters.InfosForSThread import get_wish_filters_settings, get_camera_settings, get_image_settings, \
    get_project_settings, get_filter_settings
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

        self.eof = EphemObserverFactory()
        self.obs = None

        self.path = None
        self.tempo = None

        self.img = None

        self.selected_filter = None
        self.dark_or_open = "Closed"
        self.one_photo = None

        self.for_headers_dic = {}

        self.lock = Locker()
        self.info = []

        self.filter_split_label = None

        self.count_aux = 0
        self.kwargs = None

        self.roda_filtros = FilterControl()

    def set_config_take_image(self):
        """
        seta as configuracoes para se tirar uma foto
        """
        try:
            info_cam = get_camera_settings()
            self.for_headers_dic['Set Temperature'] = info_cam[0]
            self.for_headers_dic['????Tempo de espera'] = info_cam[1]

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
                self.get_image_png = True

            try:
                self.get_image_tif = info_image[8]
            except Exception as e:
                print("self.get_image_tif = True -> {}".format(e))
                self.get_image_tif = True

            try:
                self.get_image_fit = info_image[9]
            except Exception as e:
                print("self.get_image_fit = True -> {}".format(e))
                self.get_image_fit = True

            try:
                self.filter_split_label = get_filter_settings()
            except Exception as e:
                print("get_filter_settings() -> {}".format(e))

            try:
                self.append_camera_settings()
            except Exception as e:
                print("self.append_camera_settings() in set_config_take_image -> {}".format(e))

        except Exception as e:
            print("Try ini definitive -> {}".format(e))

    def recebe_argumento(self, kwargs):
        self.kwargs = kwargs

    def args_one_photo(self, filter_args, kwargs):
        self.selected_filter = filter_args
        self.kwargs = kwargs
        self.one_photo = True
        print("\n\nargs_one_photo: ")
        print("self.selected_filter = " + str(self.selected_filter))
        print("self.dark_or_open = " + str(self.dark_or_open))
        print("self.one_photo = " + str(self.one_photo))

    def run(self):
        if self.kwargs == 0:
            try:
                self.create_image_open()
            except Exception as e:
                print("self.create_image_open() -> {}".format(e))
        else:
            try:
                self.create_image_close()
            except Exception as e:
                print("self.create_image_close() -> {}".format(e))

    def create_image_open(self):
        self.roda_filtros.open_shutter()
        self.set_config_take_image()
        self.lock.set_acquire()

        my_list = get_wish_filters_settings()  # list of schedule

        try:
            if self.count_aux < len(my_list):
                if self.one_photo:
                    index_of_dic = self.selected_filter
                else:
                    index_of_dic = str(my_list[self.count_aux])
                self.valores_principais_wish_filter(index_of_dic)
                self.count_aux += 1

            else:
                self.count_aux = 0
                if self.one_photo:
                    index_of_dic = self.selected_filter
                else:
                    index_of_dic = str(my_list[self.count_aux])
                self.valores_principais_wish_filter(index_of_dic)
                self.count_aux += 1

        except Exception as e:
            print("Try filter ini -> {}".format(e))

        project_infos = get_project_settings()

        name_observatory = project_infos[2][1]

        self.path, self.tempo = set_path()

        image_name = self.path + str(self.prefix) + "_" + str(name_observatory) + "_" + str(self.tempo)

        try:
            self.img = SbigDriver.photoshoot(self.exposure_time, self.binning, self.dark_photo)
        except Exception as e:
            print("self.img = SbigDriver.photoshoot ERROR -> " + str(e))

        self.for_headers_dic['Open or close shutter'] = "OPEN"

        self.save_image_format(image_name)

        self.for_headers_dic = {}
        self.one_photo = False
        self.lock.set_release()

    def create_image_close(self):
        self.roda_filtros.close_shutter()

        my_list = get_wish_filters_settings()  # list of schedule
        my_list = set(my_list)
        my_list = sorted(my_list)

        count_aux = 0

        while count_aux < len(my_list):
            self.set_config_take_image()
            self.lock.set_acquire()

            if self.one_photo:
                index_of_dic = self.selected_filter
                count_aux = 10
            else:
                index_of_dic = str(my_list[self.count_aux])

            self.valores_principais_wish_filter(index_of_dic)

            project_infos = get_project_settings()

            name_observatory = project_infos[2][1]

            self.path, self.tempo = set_path()

            image_name = self.path + "DARK-" + str(self.prefix) + "_" + str(name_observatory) + "_" + str(self.tempo)

            try:
                self.img = SbigDriver.photoshoot(self.exposure_time, self.binning, 1)
            except Exception as e:
                print("self.img = SbigDriver.photoshoot ERROR -> " + str(e))

            self.for_headers_dic['Open or close shutter'] = "CLOSED"

            self.save_image_format(image_name)

            self.for_headers_dic = {}
            count_aux += 1
            self.one_photo = False
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

    def save_image_format(self, image_name):
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        self.for_headers_dic['Start Time'] = self.tempo

        try:
            self.temperatura = SbigDriver.get_temperature()
            self.temperatura = "{0:.2f}".format(float(self.temperatura[3]))
            # self.temperatura = "25"
            self.for_headers_dic['Temperature'] = self.temperatura
        except Exception as e:
            print("Exception self.temperatura -> {}".format(e))
            self.for_headers_dic['Temperature'] = "???"

        if self.get_image_png:
            try:
                save_png(self.img, image_name, self.for_headers_dic)
            except Exception as e:
                print("Exception save_png() -> {}".format(e))
        if self.get_image_tif:
            try:
                save_tif(self.img, image_name)
            except Exception as e:
                print("Exception save_tif() -> {}".format(e))
        if self.get_image_fit:
            try:
                save_fit(self.img, image_name, self.for_headers_dic)
            except Exception as e:
                print("Exception save_fit() -> {}".format(e))
        if not self.get_image_fit and not self.get_image_tif and not self.get_image_fit:
            try:
                save_png(self.img, image_name, self.for_headers_dic)
            except Exception as e:
                print("Exception save_png() -> {}".format(e))

        try:
            data, hora = get_date_hour(self.tempo)
            self.info = self.path, self.img, data, hora
            self.init_image()
        except Exception as e:
            print("run init_image() -> {}".format(e))

    def valores_principais_wish_filter(self, index_of_dic):
        aux = self.filter_split_label[str(index_of_dic)][0]

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

        self.filter_wheel_control(int(aux[4]))

        self.append_filters_settings(aux)

    def append_camera_settings(self):
        try:
            project_infos = get_project_settings()

            try:
                self.obs = self.eof.create_observer(longitude=project_infos[0][1],
                                                    latitude=project_infos[0][0],
                                                    elevation=project_infos[1][0])

                now_datetime = datetime.utcnow()
                self.obs.date = ephem.date(now_datetime)

                sun = ephem.Sun(self.obs)

                moon = ephem.Moon(self.obs)
                frac = moon.moon_phase

                sun_alt = ephem.degrees(sun.alt)
                moon_alt = ephem.degrees(moon.alt)

                sun_elevation = "{:.2f}".format(float(math.degrees(sun_alt)))
                moon_elevation = "{:.2f}".format(float(math.degrees(moon_alt)))
                moon_phase = "{0:.2f}".format(frac * 100)
            except Exception as e:
                print("ephem update -> {}".format(e))

            self.for_headers_dic['Latitude'] = str(project_infos[0][0])
            self.for_headers_dic['Longitude'] = str(project_infos[0][1])
            self.for_headers_dic['Elevation(m)'] = str(project_infos[0][2])
            self.for_headers_dic['Pressure(mb)'] = str(project_infos[0][3])
            self.for_headers_dic['Sun Elevation'] = str(sun_elevation)
            self.for_headers_dic['Ignore Lunar Position'] = str(project_infos[1][1])
            self.for_headers_dic['Moon Elevation'] = str(moon_elevation)
            self.for_headers_dic['Moon Phase'] = str(moon_phase)
            self.for_headers_dic['Name'] = str(project_infos[2][0])
            self.for_headers_dic['Observatory'] = str(project_infos[2][1])
            self.for_headers_dic['Imager ID'] = str(project_infos[2][2])
            self.for_headers_dic['get_level1'] = str(self.get_level1)
            self.for_headers_dic['get_level2'] = str(self.get_level2)
            self.for_headers_dic['get_axis_xi'] = str(self.get_axis_xi)
            self.for_headers_dic['get_axis_xf'] = str(self.get_axis_xf)
            self.for_headers_dic['get_axis_yi'] = str(self.get_axis_yi)
            self.for_headers_dic['get_axis_yf'] = str(self.get_axis_yf)
            self.for_headers_dic['get_ignore_crop'] = str(self.get_ignore_crop)
        except Exception as e:
            print("run append_camera_settings() -> {}".format(e))

    def append_filters_settings(self, aux):
        try:
            self.for_headers_dic['Filter Label'] = str(aux[0])
            self.for_headers_dic['Filter Wavelength'] = str(aux[1])
            self.for_headers_dic['Exposure'] = str(self.exposure_time)
            self.for_headers_dic['Binning'] = str(aux[3])
            self.for_headers_dic['Filter Position'] = str(aux[4])
        except Exception as e:
            print("run append_filters_settings() -> {}".format(e))
