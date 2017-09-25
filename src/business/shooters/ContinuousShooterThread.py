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
        self.dark_sthread.started.connect(self.dark_thread_iniciada)

        self.ss.started.connect(self.thread_iniciada)
        self.console = ConsoleThreadOutput()
        self.count = 0

        self.wait_temperature = False
        self.not_two_dark = True
        self.one_photo = False

    def run(self):
        self.count = 1
        try:
            self.dark_sthread.start()
            while self.dark_sthread.isRunning():
                time.sleep(1)
            else:
                self.count = 1
                while self.continuous:
                    try:
                        self.signal_temp.emit()
                        if self.wait_temperature:
                            self.ss.start()
                            while self.ss.isRunning():
                                time.sleep(1)
                    except Exception as e:
                        print(e)
                    finally:
                        self.dark_sthread.start()
                        while self.dark_sthread.isRunning():
                            time.sleep(1)
                    time.sleep(1)
                    self.signalAfterShooting.emit()
        except Exception as e:
            print("Exception dark_sthread ->" + str(e))

    def start_continuous_shooter(self):
        self.continuous = True

    def stop_continuous_shooter(self):
        self.wait_temperature = False
        self.continuous = False
        self.not_two_dark = False
        self.console.raise_text("Taking dark photo", 1)
        self.ss.take_dark()
        time.sleep(1)
        self.count = 1

    def stop_one_photo(self):
        self.one_photo = False
        self.wait_temperature = False
        self.continuous = False
        self.count = 1

    def thread_iniciada(self):
        self.console.raise_text("Taking photo N: {}".format(self.count), 1)
        self.count += 1

    def dark_thread_iniciada(self):
        self.console.raise_text("Taking dark photo N: {}".format(self.count), 1)
        self.count += 1
