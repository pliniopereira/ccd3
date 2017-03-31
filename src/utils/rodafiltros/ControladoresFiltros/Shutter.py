from time import sleep


class Shutter(object):
    def open_shutter(self):
        try:
            self.WriteCommand("UB=1")  # Make sure shutter is in the closed state
            sleep(1)
        except Exception as e:
            print(e)

    def close_shutter(self):
        try:
            self.WriteCommand("UB=0")
            sleep(1)
        except Exception as e:
            print(e)
