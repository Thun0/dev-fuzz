from adb.client import Client as AdbClient
from settings import config
from android.device import Device


def get_devices():
    devices = []
    client = AdbClient(host="127.0.0.1", port=config['adb_port'])
    for d in client.devices():
        devices.append(Device(d.serial))
    return devices
