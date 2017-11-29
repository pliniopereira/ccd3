import os

import skimage.io
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from pyfits import getdata
from scipy.misc import toimage

from src.controller.Camera import Camera
from src.ui.commons.layout import set_hbox, set_lvbox
from src.utils.camera import Image_Processing


# Aux Functions
def set_width(*s):
    for o in s:
        o.setMaximumWidth(25)
        o.setMaxLength(2)


class Shooter(QtWidgets.QWidget):
    """
    Class for Taking photo Widget
    """

    def __init__(self, parent=None):
        super(Shooter, self).__init__(parent)
        self.cam = Camera()
        self.cond = 0

        # Label for Image
        self.img = QtWidgets.QLabel(self)
        self.config_img_label()

        # Creating a Pallete
        self.pa = QtGui.QPalette()

        self.set_layout()
        self.link_signals()

    def link_signals(self):
        self.cam.ephemerisShooterThread.continuousShooterThread.ss.finished.connect(self.get_image_automatic)
        self.cam.continuousShooterThread.ss.finished.connect(self.get_image_manual)

    def get_image_automatic(self):
        img = self.cam.ephemerisShooterThread.continuousShooterThread.ss.get_image_info()
        self.set_image(img)

    def get_image_manual(self):
        img = self.cam.continuousShooterThread.ss.get_image_info()
        self.set_image(img)

    def set_layout(self):
        hb2 = set_hbox(self.prefix, self.date, self.hour)

        self.setLayout(set_lvbox(set_hbox(self.img), hb2))
        self.config_pallete()

    def config_img_label(self):
        self.img.setPixmap(QtGui.QPixmap("noimage.png"))
        self.prefix = QtWidgets.QLabel(self)
        self.date = QtWidgets.QLabel(self)
        self.hour = QtWidgets.QLabel(self)

    def config_pallete(self):
        self.pa.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)  # Setting the style
        self.prefix.setPalette(self.pa)
        self.date.setPalette(self.pa)
        self.hour.setPalette(self.pa)

    def shoot_function(self):
        self.cam.shoot(int(self.tb.text()), self.pre.text(), int(self.combo.currentIndex()))
        self.set_image()

    def auto_shoot(self):
        try:
            self.cam.autoshoot(int(self.htext.text()), int(self.mtext.text()), int(self.tb.text()), self.pre.text(),
                               int(self.combo.currentIndex()))
        except Exception as e:
            print(e)

    def set_image(self, img):
        print("Setting Pixmap")
        print("CCCCCCCCCCCCCCCCCCCCCCCCCCC")
        try:
            path = img.path + img.name_image + ".fit"
            str_name_image = str(img.name_image + ".fit")

            # image = Image.open(path)]

            try:
                if os.path.splitext(path)[1] == '.fit':
                    print("1111111111111111111")
                    img = getdata(path)
                else:
                    print("222222222222222222222")
                    img = skimage.io.imread(path)

                print("\n\n>>>>>>>>>>>>>>>>>>>>>>")
                print(img)

            except Exception as e:
                print("Exception os.path.splitext -> {}".format(e))

            file_name = path


            image = img

            get_level1 = 0.00

            get_level2 = 0.99

            # variavel = Image_Processing.get_level(image, get_level1, get_level2)
            #
            # im2 = Image_Processing.bytscl(image, variavel[1], variavel[0])

            im3 = toimage(image)

            # im4 = Image_Processing.resize_image_512x512(im3)

            im4 = im3.resize((int(512), int(512)))
            im5 = Image_Processing.draw_image(im4, str_name_image)

            # try:
            #     im5 = Image_Processing.draw_image(im4, str_name_image)
            #
            #     # im5.show()
            # except Exception as e:
            #     print("Exception image_processing... -> {}".format(e))

            try:
                qim = ImageQt(im5)
                self.img.setPixmap(QtGui.QPixmap.fromImage(qim))
            except Exception as e:
                print("Exception setPixmap(QtGui.QPixmap(image_to_show)) -> {}".format(e))

            print(path)

        except Exception as e:
            print("Exception Setting Pixmap -> {}".format(e))

    def fill_combo(self):
        self.combo.addItem("1x1", 0)
        self.combo.addItem("2x2", 1)
        self.combo.addItem("3x3", 2)

    def clear_image_info(self):
        self.prefix.clear()
