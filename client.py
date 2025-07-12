from adbutils import adb
from numpy import asarray


class Client:
    def __init__(self, serial):
        self.serial = serial
        self.device = adb.device(serial=self.serial)

    def capture_screen(self, asarray_output=True):
        if asarray_output:
            return asarray(self.device.screenshot())
        else:
            return self.device.screenshot()

    def click(self, point):
        self.device.click(point[0], point[1])
