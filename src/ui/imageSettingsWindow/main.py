from PyQt5 import QtWidgets

from src.ui.imageSettingsWindow.SettingsImageWindow import SettingsImageWindow


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.a = SettingsImageWindow(self)
        self.setCentralWidget(self.a)

        self.setWindowTitle("Image Settings")
