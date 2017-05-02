from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QMenu, QPushButton, QVBoxLayout, QWidget)

from src.utils.camera.SbigDriver import (ccdinfo)


class SettingsImager(QWidget):
    def __init__(self, parent=None):
        super(SettingsImager, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.createFilterWheelGroup(), 0, 0)
        grid.addWidget(self.createCCDCameraGroup(), 1, 0)
        grid.addWidget(self.createPushButtonGroup(), 2, 0)
        self.setLayout(grid)

        self.setWindowTitle("Imager Box")
        self.resize(500, 340)

    def createFilterWheelGroup(self):
        groupBox = QGroupBox("FILTERWHEEL")

        radio1 = QtWidgets.QLabel("Serial Port: COM1", self)
        #radio1.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        radio2 = QtWidgets.QLabel("Filter Slots: 6", self)
        #radio2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        radio3 = QtWidgets.QLabel("Filter Setpoint Temp: 25", self)
        #radio3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #radio1 = QtWidgets.QLabel("&Radio button 1")
        #radio2 = QRadioButton("R&adio button 2")
        #radio3 = QRadioButton("Ra&dio button 3")

        #radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createCCDCameraGroup(self):
        groupBox = QGroupBox("CCD Camera Options")
        groupBox.setCheckable(True)
        groupBox.setChecked(False)

        radio1 = QtWidgets.QLabel("Camera Port: USB", self)
        radio2 = QtWidgets.QLabel("Camera Name", self)

        radio3 = QtWidgets.QLabel("CCD Temperature Setpoint:", self)
        radio4 = QtWidgets.QLabel("Temp Set Point", self)
        radio5 = QtWidgets.QLabel("Shutter:", self)
        radio6 = QtWidgets.QLabel("Tempo para iniciar:", self)
        label = QtWidgets.QLabel("     Label Text Value: ", self)
        label.setFixedWidth(200)

        textEdit = QtWidgets.QTextEdit(self)
        textEdit.setMaximumHeight(55)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addWidget(radio4)
        vbox.addWidget(radio5)
        vbox.addWidget(radio6)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createPushButtonGroup(self):
        groupBox = QGroupBox("&Push Buttons")
        groupBox.setCheckable(True)
        groupBox.setChecked(True)

        pushButton = QPushButton("&Normal Button")
        toggleButton = QPushButton("&Toggle Button")
        toggleButton.setCheckable(True)
        toggleButton.setChecked(True)
        flatButton = QPushButton("&Flat Button")
        flatButton.setFlat(True)

        popupButton = QPushButton("Pop&up Button")
        menu = QMenu(self)
        menu.addAction("&First Item")
        menu.addAction("&Second Item")
        menu.addAction("&Third Item")
        menu.addAction("F&ourth Item")
        popupButton.setMenu(menu)

        newAction = menu.addAction("Submenu")
        subMenu = QMenu("Popup Submenu", self)
        subMenu.addAction("Item 1")
        subMenu.addAction("Item 2")
        subMenu.addAction("Item 3")
        newAction.setMenu(subMenu)

        vbox = QVBoxLayout()
        vbox.addWidget(pushButton)
        vbox.addWidget(toggleButton)
        vbox.addWidget(flatButton)
        vbox.addWidget(popupButton)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def get_info_pixels(self):
        '''
        Function to get the CCD Info
        This function will return [Pixels]
        '''
        ret = None
        self.lock.set_acquire()
        try:
            ret = tuple(ccdinfo())
        except Exception as e:
            self.console.raise_text("Failed to get camera information.\n{}".format(e))
        finally:
            self.lock.set_release()
        return ret