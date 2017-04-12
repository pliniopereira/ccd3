from PyQt5 import QtWidgets

from src.ui.filterWindow.filterWindow import FilterWindow


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.f = FilterWindow(self)
        self.setCentralWidget(self.f)

        self.setWindowTitle("Filters Settings")
