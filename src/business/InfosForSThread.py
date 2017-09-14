from src.business.configuration.settingsCamera import SettingsCamera
from src.business.configuration.settingsImage import SettingsImage
from src.business.sequence_filters.SettingsSequenceFilters import SettingsSequenceFilters
from src.business.shooters import LabelFilters
from src.utils.camera.Image_Processing import get_observatory


def get_wish_filters_settings():
    settings = SettingsSequenceFilters()
    info_wish_filters = settings.get_sequence_filters_settings()

    my_list = []
    available_filters = LabelFilters.get_filter_settings()
    available_filters_list = list(available_filters)

    for i, c in enumerate(info_wish_filters):
        if c in available_filters_list:
            my_list.append(c)

    return my_list


def get_project_settings():
    from src.business.configuration.configProject import ConfigProject
    ci = ConfigProject()
    name_geographic_settings = str(ci.get_geographic_settings())
    name_set_moonsun_settings = str(ci.get_moonsun_settings())
    name_site_settings = str(ci.get_site_settings())

    name_observatory = get_observatory(name_site_settings)

    return name_geographic_settings, name_set_moonsun_settings, name_site_settings


def get_image_settings():
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


def get_camera_settings():
    """
    Pega os valores no ini camera
    info_cam[0] = temperature_camera
    info_cam[1] = tempo de espera até atingir temperatura desejada
    info_cam[2] = dark(Open or close shutter)
    """
    settings = SettingsCamera()
    info_cam = settings.get_camera_settings()

    return info_cam
