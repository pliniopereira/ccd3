from PyQt5 import QtCore
from PyQt5 import QtWidgets

from src.ui.CCDWindow.SettingsCCDInfos import SettingsCCDInfos


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.ima = SettingsCCDInfos(self)

        self.setCentralWidget(self.ima)

        self.setWindowTitle("Imager Settings")

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

    def show_camera_infos(self):
        try:
            self.ima.info_cam()
        except Exception as e:
            print("show_camera_infos on menu -> {}".format(e))

