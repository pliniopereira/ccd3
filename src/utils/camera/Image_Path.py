from datetime import datetime

from src.utils.camera import Image_Processing
from src.utils.camera.Julian_Day import jd_to_date, date_to_jd


def set_path():
    tempo = datetime.utcnow().strftime('%Y%m%d_%H%M%S')

    data = tempo[0:4] + "_" + tempo[4:6] + tempo[6:8]

    from src.business.configuration.configSystem import ConfigSystem
    cs = ConfigSystem()
    path = str(cs.get_image_path()) + "/"

    from src.business.configuration.configProject import ConfigProject
    ci = ConfigProject()
    name_observatory = str(ci.get_site_settings())
    name_observatory = Image_Processing.get_observatory(name_observatory)

    if int(tempo[9:11]) > 12:
        path = path + name_observatory + "_" + data + "/"
    else:
        ano = tempo[0:4]
        mes = tempo[4:6]
        dia = tempo[6:8]
        abs_julian_day = jd_to_date(date_to_jd(ano, mes, int(dia)) - 1)

        mes = abs_julian_day[1]
        dia = abs_julian_day[2]
        ano = abs_julian_day[0]

        if 0 < int(dia) < 10:
            dia = "0" + str(dia)
        if 0 < int(mes) < 10:
            mes = "0" + str(mes)

        path = path + name_observatory + "_" + str(ano) + "_" + str(mes) + str(dia) + "/"

    return path, tempo


def get_observatory(name):
    name_aux = str(name).split(',')[1]
    name_aux = name_aux.replace("/", "")
    name_aux = name_aux.replace(" ", "")

    return name_aux
