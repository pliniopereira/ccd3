import time

from PyQt5 import QtCore

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.shooters.SThread import SThread


class ContinuousShooterThread(QtCore.QThread):
    # classe para modo manual

    signalAfterShooting = QtCore.pyqtSignal(name="signalAfterShooting")
    signal_temp = QtCore.pyqtSignal(name="signalTemp")

    def __init__(self, time_sleep):
        super(ContinuousShooterThread, self).__init__()
        self.continuous = True

        # SThread manda para o Sbigdriver as informações para se tirar a foto em si.

        self.ss = SThread()

        self.photo_type = self.ss.recebe_argumento

        self.ss.started.connect(self.thread_iniciada)
        self.console = ConsoleThreadOutput()
        self.count = 0

        self.wait_temperature = False
        self.not_two_dark = True
        self.one_photo = False

        self.one_photo_shutter_state = None

        self.select_filter_manual = None
        self.select_filter_shutter = None

    def recebe_args(self, select_filter_manual, select_filter_shutter):
        self.select_filter_manual = select_filter_manual
        self.select_filter_shutter = select_filter_shutter
        self.one_photo = True

    def run(self):
        try:
            self.count = 1
            while self.continuous:
                try:
                    self.signal_temp.emit()
                    if self.wait_temperature:
                        if self.count <= 1 and not self.one_photo:
                            self.console.raise_text("Taking dark photo", 1)
                            self.start_dark_sthread()

                        if self.select_filter_shutter == "Closed" and self.one_photo:
                            self.ss.recebe_argumento(1)
                        else:
                            self.ss.recebe_argumento(0)

                        if self.one_photo:
                            self.ss.args_one_photo(self.select_filter_manual, self.select_filter_shutter)

                        self.ss.start()
                        if self.one_photo:
                            break
                        while self.ss.isRunning():
                            time.sleep(1)
                except Exception as e:
                    print(e)
                time.sleep(1)
                self.signalAfterShooting.emit()
        except Exception as e:
            print("Exception Run ContinuousShooterThread ->" + str(e))
        finally:
            if not self.one_photo:
                self.console.raise_text("Taking dark photo", 1)
                self.start_dark_sthread()
            self.one_photo = False

    def start_continuous_shooter(self):
        self.continuous = True

    def stop_continuous_shooter(self):
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
        if self.one_photo:
            self.console.raise_text("Taking photo", 1)
            self.stop_one_photo()
        else:
            self.console.raise_text("Taking photo N: {}".format(self.count), 1)
            self.count += 1

    def start_dark_sthread(self):
        if not self.one_photo:
            try:
                self.ss.recebe_argumento(1)
                self.ss.start()
                while self.ss.isRunning():
                    time.sleep(1)
            except Exception as e:
                print("Error start_dark_sthread! {}".format(e))
                self.console.raise_text("Error start_dark_sthread! {}".format(e), 3)
            finally:
                self.count = 1
