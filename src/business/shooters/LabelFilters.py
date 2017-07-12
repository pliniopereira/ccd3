from src.business.filters.settingsFilters import SettingsFilters


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

    for i in range(n):
        start = int(i * len_l / n)
        end = int((i + 1) * len_l / n)
        filter_split_l.append(info_filters_l[start:end])

    return filter_split_l