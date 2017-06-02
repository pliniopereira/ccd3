from PyQt5.QtGui import QIntValidator, QDoubleValidator


class ValidatorFactory:
    def __init__(self):
        pass

    def create_validator_int_from_0_to_1000(self):
        qiv = QIntValidator()
        qiv.setRange(0, 1000)
        return qiv

    def create_validator_int_from_minus_100_to_100(self):
        qiv = QIntValidator()
        qiv.setRange(-100, 100)
        return qiv

    def create_validator_int_from_0_to_360(self):
        qiv = QIntValidator()
        qiv.setRange(0, 360)
        return qiv

    def create_validator_double_from_minus_100_to_100(self):
        qiv = QDoubleValidator()
        qiv.setRange(-100, 100)
        return qiv
