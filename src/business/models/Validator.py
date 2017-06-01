from PyQt5 import QtGui


class Validator:

    def __init__(self):
        self.objValidator = None

        self.intValidator = QtGui.QIntValidator()
        self.intValidator.setRange(0, 1000)

        self.neg_intValidator = QtGui.QIntValidator()
        self.neg_intValidator.setRange(-50, 100)

        self.doubleValidator = QtGui.QDoubleValidator()
        self.doubleValidator.setRange(0.0, 1000.0, 5)

