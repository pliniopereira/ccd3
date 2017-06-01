from PyQt5.QtGui import QIntValidator, QDoubleValidator


class Validator:

    def __init__(self):
        self.intValidator = QIntValidator()
        self.intValidator.setRange(0, 1000)

        self.neg_intValidator = QIntValidator()
        self.neg_intValidator.setRange(-50, 100)

        self.doubleValidator = QDoubleValidator()
        self.doubleValidator.setRange(-100, 1000)
        # self.doubleValidator.bottom(0.99)
        # self.doubleValidator.top(100.99)
        # self.doubleValidator.decimals(2)

        self.neg_doubleValidator = QDoubleValidator()
        self.neg_doubleValidator.setRange(-100.0, 1000.0, 5)
