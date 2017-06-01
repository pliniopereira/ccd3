from PyQt5 import QtCore

from src.business.filters.constants import filters as f
from src.business.consoleThreadOutput import ConsoleThreadOutput


class SettingsFilters:
    def __init__(self):
        self._settings = QtCore.QSettings()
        self.setup_settings()
        self.console = ConsoleThreadOutput()

    def setup_settings(self):
        self._settings = QtCore.QSettings(f.FILTERSFILE, QtCore.QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

    def save_settings(self):
        self._settings.sync()

    def set_filters_settings(self,
                             label_filter1, wavelength_filter1, exposure_filter1, binning_filter1, ccdgain_filter1,
                             label_filter2, wavelength_filter2, exposure_filter2, binning_filter2, ccdgain_filter2,
                             label_filter3, wavelength_filter3, exposure_filter3, binning_filter3, ccdgain_filter3,
                             label_filter4, wavelength_filter4, exposure_filter4, binning_filter4, ccdgain_filter4,
                             label_filter5, wavelength_filter5, exposure_filter5, binning_filter5, ccdgain_filter5,
                             label_filter6, wavelength_filter6, exposure_filter6, binning_filter6, ccdgain_filter6):

        self._settings.setValue(f.LABEL_FILTER1, label_filter1)
        self._settings.setValue(f.WAVELENGTH_FILTER1, wavelength_filter1)
        self._settings.setValue(f.EXPOSURE_FILTER1, exposure_filter1)
        self._settings.setValue(f.BINNING_FILTER1, binning_filter1)

        self._settings.setValue(f.LABEL_FILTER2, label_filter2)
        self._settings.setValue(f.WAVELENGTH_FILTER2, wavelength_filter2)
        self._settings.setValue(f.EXPOSURE_FILTER2, exposure_filter2)
        self._settings.setValue(f.BINNING_FILTER2, binning_filter2)

        self._settings.setValue(f.LABEL_FILTER3, label_filter3)
        self._settings.setValue(f.WAVELENGTH_FILTER3, wavelength_filter3)
        self._settings.setValue(f.EXPOSURE_FILTER3, exposure_filter3)
        self._settings.setValue(f.BINNING_FILTER3, binning_filter3)

        self._settings.setValue(f.LABEL_FILTER4, label_filter4)
        self._settings.setValue(f.WAVELENGTH_FILTER4, wavelength_filter4)
        self._settings.setValue(f.EXPOSURE_FILTER4, exposure_filter4)
        self._settings.setValue(f.BINNING_FILTER4, binning_filter4)

        self._settings.setValue(f.LABEL_FILTER5, label_filter5)
        self._settings.setValue(f.WAVELENGTH_FILTER5, wavelength_filter5)
        self._settings.setValue(f.EXPOSURE_FILTER5, exposure_filter5)
        self._settings.setValue(f.BINNING_FILTER5, binning_filter5)

        self._settings.setValue(f.LABEL_FILTER6, label_filter6)
        self._settings.setValue(f.WAVELENGTH_FILTER6, wavelength_filter6)
        self._settings.setValue(f.EXPOSURE_FILTER6, exposure_filter6)
        self._settings.setValue(f.BINNING_FILTER6, binning_filter6)

    def get_filters_settings(self):
        return self._settings.value(f.LABEL_FILTER1), \
               self._settings.value(f.WAVELENGTH_FILTER1), \
               self._settings.value(f.EXPOSURE_FILTER1), \
               self._settings.value(f.BINNING_FILTER1), \
               self._settings.value(f.LABEL_FILTER2), \
               self._settings.value(f.WAVELENGTH_FILTER2), \
               self._settings.value(f.EXPOSURE_FILTER2), \
               self._settings.value(f.BINNING_FILTER2), \
               self._settings.value(f.LABEL_FILTER3), \
               self._settings.value(f.WAVELENGTH_FILTER3), \
               self._settings.value(f.EXPOSURE_FILTER3), \
               self._settings.value(f.BINNING_FILTER3), \
               self._settings.value(f.LABEL_FILTER4), \
               self._settings.value(f.WAVELENGTH_FILTER4), \
               self._settings.value(f.EXPOSURE_FILTER4), \
               self._settings.value(f.BINNING_FILTER4), \
               self._settings.value(f.LABEL_FILTER5), \
               self._settings.value(f.WAVELENGTH_FILTER5), \
               self._settings.value(f.EXPOSURE_FILTER5), \
               self._settings.value(f.BINNING_FILTER5), \
               self._settings.value(f.LABEL_FILTER6), \
               self._settings.value(f.WAVELENGTH_FILTER6), \
               self._settings.value(f.EXPOSURE_FILTER6), \
               self._settings.value(f.BINNING_FILTER6)

    def get_filepath(self):
        return self._settings.value(f.FILTERSFILE)
