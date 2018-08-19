import configparser
from fuzzer import Fuzzer
from android import utils
import settings
from utils import terminal
import threading
from pathlib import Path


class Project:

    def __init__(self, name=''):
        self.name = name
        self.filepath = ''
        self.devices = []
        self.devpath = ''
        self.corpuspath = None
        self.fuzzers = []
        self.error = None
        self.threads = []

    def create(self, path):
        self.filepath = path
        Path(self.filepath).touch(0o644)
        p = Path(self.filepath).absolute().parents[0]
        suffix = self.filepath.split('/')[-1].split('.')[0]
        pp = p/suffix
        idx = 1
        while pp.exists():
            pp = p/'{}{}'.format(suffix, idx)
            idx += 1

        self.corpuspath = str(pp)
        pp.mkdir(0o755)
        p1 = pp / 'ioctl'
        p2 = pp / 'write'
        p3 = pp / 'mmap'
        p1.mkdir(0o755)
        p2.mkdir(0o755)
        p3.mkdir(0o755)
        self.save()

    def load(self, path):
        self.filepath = path
        config = configparser.ConfigParser()
        config.read_file(open(self.filepath))
        self.name = config['project']['name']
        self.devpath = config['project']['devpath']
        self.corpuspath = config['project']['corpuspath']

    def save(self):
        config = configparser.ConfigParser()
        config['project'] = {}
        config['project']['name'] = self.name
        config['project']['devpath'] = self.devpath
        config['project']['corpuspath'] = self.corpuspath
        with open(self.filepath, 'w') as conf_file:
            config.write(conf_file)
        print('Projekt zostal zapisany!')

    def main_menu(self):
        while True:
            terminal.clear()
            if self.error:
                terminal.red()
                print(self.error)
                terminal.end_color()
                self.error = None
            print('Projekt {}'.format(self.name))
            print('--------------------')
            print('1. Rozpocznij test sterownika')
            print('--------------------')
            if self.devpath:
                print('2. Wybierz sterownik (wybrano {})'.format(self.devpath))
            else:
                print('2. Wybierz sterownik')
            if self.corpuspath:
                print('3. Wybierz korpus (wybrano {})'.format(self.corpuspath))
            else:
                print('3. Wybierz korpus')
            print('4. Wybierz urzadzenia (wybrano {} urządzen)'.format(len(self.devices)))
            print('5. Zrestartuj wszystkie urzadzenia')
            print('--------------------')
            print('6. Zapisz projekt')
            print('0. Wyjscie')
            print('--------------------')
            choice = int(input('Wybor: '))
            if choice == 0:
                break
            elif choice == 1:
                self.start_test()
            elif choice == 2:
                self.choose_driver()
            elif choice == 4:
                self.choose_devices()
            elif choice == 5:
                self.reboot_devices()
            elif choice == 6:
                self.save()

    def reboot_devices(self):
        pass

    def start_test(self):
        if len(self.devices) == 0:
            self.error = 'Wybierz urzadzenia do testu!'
            return
        port = settings.config['devices_start_port']
        print('Pushing agents')
        for d in self.devices:
            d.push(settings.config['agent_path'], '/data/local/tmp/agent', 0o755)
            self.fuzzers.append(Fuzzer(d, port, self.devpath))
            port += 1
        for f in self.fuzzers:
            t = threading.Thread(target=f.run, daemon=True)
            self.threads.append(t)
            t.start()
        print('Fuzzing started!')
        print('{} active threads'.format(threading.active_count()-1))
        print('Press any key to stop testing...')
        input()
        print('Stopping..')
        for f in self.fuzzers:
            f.stop()
        for t in self.threads:
            t.join()
        self.fuzzers = []
        self.threads = []
        print('{} active threads'.format(threading.active_count()-1))

    def choose_driver(self):
        self.devpath = input('Podaj sciezke do sterownika: ')

    def choose_devices(self):
        all_devices = utils.get_devices()
        while True:
            terminal.clear()
            if len(all_devices) == 0:
                print('Brak urzadzen')
                print('--------------------')
            else:
                print('Dostepne urzadzenia: ')
                print('--------------------')
                for i in range(0, len(all_devices)):
                    chosen = ' '
                    if all_devices[i] in self.devices:
                        chosen = 'X'
                    print('[{}] {}. {}'.format(chosen, i+1, all_devices[i].serial))
                print('--------------------')
                print('1-{}. Zaznacz/odznacz urzadzenie do przeprowadzenia testu'.format(len(all_devices)))
            print('a. Odswiez liste')
            print('0. Powrot')
            print('--------------------')
            choice = input('Wybor: ')
            if choice == 'a':
                all_devices = utils.get_devices()
                continue
            try:
                choice = int(choice)
                if choice == 0:
                    break
                elif 0 < choice <= len(all_devices):
                    choice -= 1
                    if all_devices[choice] in self.devices:
                        self.devices.remove(all_devices[choice])
                    else:
                        self.devices.append(all_devices[choice])
            except ValueError:
                pass
