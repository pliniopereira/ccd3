from src.business.configuration.settingsCamera import SettingsCamera
from src.business.configuration.settingsImage import SettingsImage
from src.business.filters.settingsFilters import SettingsFilters
from src.business.sequence_filters.SettingsSequenceFilters import SettingsSequenceFilters


def get_filter_settings():
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
    filter_split_l = []
    len_l = len(info_filters_l)

    filter_position_dic = {}

    for i in range(n):
        start = int(i * len_l / n)
        end = int((i + 1) * len_l / n)
        filter_split_l.append(info_filters_l[start:end])

    i = 0
    x = 1
    n = len(filter_split_l)
    list(filter_split_l)
    while i < n:
        try:
            if filter_split_l[i][0] == '' or filter_split_l[i][2] == '':
                filter_split_l[i] = list(filter_split_l[i])
                filter_split_l = list(filter_split_l)
                filter_split_l.remove(filter_split_l[i])
                i -= 1
                n -= 1
                x += 1
            else:
                filter_split_l[i] = list(filter_split_l[i])
                filter_split_l[i].extend(str(x))
                x += 1
        except Exception as e:
            print(e)
        i += 1

    dic = {}
    for lista in filter_split_l:
        dic[lista[4]] = []
        dic[lista[4]].append(lista)

    return dic


def get_wish_filters_settings():
    settings = SettingsSequenceFilters()
    info_wish_filters = settings.get_sequence_filters_settings()

    my_list = []
    available_filters = get_filter_settings()
    available_filters_list = list(available_filters)

    for i, c in enumerate(info_wish_filters):
        if c in available_filters_list:
            my_list.append(c)

    return my_list


def get_project_settings():
    from src.business.configuration.configProject import ConfigProject
    ci = ConfigProject()

    name_geographic_settings = ci.get_geographic_settings()
    name_set_moonsun_settings = ci.get_moonsun_settings()
    name_site_settings = ci.get_site_settings()

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
    print("\n\n")
    print("type(info_cam)")
    print(type(info_cam))
    print("\n\n")

    return info_cam
