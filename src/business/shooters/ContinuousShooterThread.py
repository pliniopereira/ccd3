import time

from PyQt5 import QtCore

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.shooters.SThread import SThread
from src.business.shooters.Dark_SThread import Dark_SThread


class ContinuousShooterThread(QtCore.QThread):
    # classe para modo manual

    signalAfterShooting = QtCore.pyqtSignal(name="signalAfterShooting")
    signal_temp = QtCore.pyqtSignal(name="signalTemp")

    def __init__(self, time_sleep):
        super(ContinuousShooterThread, self).__init__()
        self.continuous = True

        # SThread manda para o Sbigdriver as informações para se tirar a foto em si.

        self.ss = SThread()

        self.dark_sthread = Dark_SThread()

        self.ss.started.connect(self.thread_iniciada)
        self.console = ConsoleThreadOutput()
        self.count = 0

        self.wait_temperature = False
        self.not_two_dark = True
        self.one_photo = False

    def run(self):
        try:
            self.count = 1
            while self.continuous:
                try:
                    self.signal_temp.emit()
                    if self.wait_temperature:
                        if self.count <= 1:
                            self.console.raise_text("Taking dark photo", 1)
                            self.start_dark_sthread()
                        self.ss.start()
                        while self.ss.isRunning():
                            time.sleep(1)
                except Exception as e:
                    print(e)
                time.sleep(1)
                self.signalAfterShooting.emit()
        except Exception as e:
            print("Exception Run ContinuousShooterThread ->" + str(e))

    def start_continuous_shooter(self):
        self.continuous = True

    def stop_continuous_shooter(self):
        self.start_dark_sthread()
        self.wait_temperature = False
        self.continuous = False
        self.not_two_dark = False
        # self.console.raise_text("Taking dark photo", 1)
        self.count = 1

    def stop_one_photo(self):
        self.one_photo = False
        self.wait_temperature = False
        self.continuous = False
        self.count = 1

    def thread_iniciada(self):
        self.console.raise_text("Taking photo N: {}".format(self.count), 1)
        self.count += 1

    def start_dark_sthread(self):
        try:
            self.console.raise_text("Taking dark photo")
            self.dark_sthread.start()
            while self.dark_sthread.isRunning():
                time.sleep(1)
        except Exception as e:
            print("Error start_dark_sthread! {}".format(e))
            self.console.raise_text("Error start_dark_sthread! {}".format(e), 3)
