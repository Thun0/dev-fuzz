from adb.client import Client as AdbClient
from settings import config
import subprocess
from android.device import AndroidDevice

def get_devices():
    adb = subprocess.Popen(['adb', '-P', str(config['adb_port']), 'start-server'], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    client = AdbClient(host="127.0.0.1", port=config['adb_port'])
    print(client)
    devs = []
    for d in client.devices():
        devs.append(AndroidDevice(d))
    return devs
