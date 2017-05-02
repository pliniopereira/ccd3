from PyQt5 import QtWidgets

from src.ui.CCDWindow.SettingsCCDInfos import SettingsCCDInfos


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.ima = SettingsCCDInfos(self)
        self.setCentralWidget(self.ima)

        self.setWindowTitle("CCD Settings")
