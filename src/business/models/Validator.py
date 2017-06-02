from PyQt5.QtGui import QIntValidator, QDoubleValidator


class Validator:

    def __init__(self):
        self.intValidator = QIntValidator()
        self.intValidator.setRange(0, 1000)

        self.neg_intValidator = QIntValidator()
        self.neg_intValidator.setRange(-101, 100)

        self.doubleValidator = QDoubleValidator()
        self.doubleValidator.setRange(-100, 1000)
