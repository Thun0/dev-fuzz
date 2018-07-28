from adb.client import Client as AdbClient


class Device:

    def __init__(self, serial):
        self.serial = serial
        self.port = -1
