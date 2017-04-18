from PyQt5 import QtWidgets

from src.ui.imagerWindow.settingsImager import SettingsImager


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.ima = SettingsImager(self)
        self.setCentralWidget(self.ima)

        self.setWindowTitle("Imager Settings")
