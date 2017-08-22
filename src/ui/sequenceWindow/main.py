from PyQt5 import QtWidgets

from src.ui.sequenceWindow.SequenceFilters import SequenceFilters


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.s = SequenceFilters(self)
        self.setCentralWidget(self.s)

        self.setWindowTitle("Acquisition Schedule")
