import subprocess
from settings import config

adb = subprocess.Popen(['adb', '-P', str(config['adb_port']), 'start-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
