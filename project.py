import configparser
from android import device
from android import utils

class Project:

    def __init__(self, name):
        self.name = name
        self.filepath = ''
        self.devices = []

    def create(self, path):
        self.filepath = path

    def load(self, path):
        pass

    def save(self):
        config = configparser.ConfigParser()
        with open(self.filepath, 'w') as conf_file:
            config.write(conf_file)

    def main_menu(self):
        while True:
            print('\033[H\033[J')
            print('Projekt {}'.format(self.name))
            print('--------------------')
            print('1. Rozpocznij test')
            print('--------------------')
            print('2. Wybierz sterownik')
            print('3. Wybierz korpus')
            print('4. Wybierz urzadzenia')
            print('--------------------')
            print('5. Zapisz projekt')
            print('0. Wyjscie')
            print('--------------------')
            choice = int(input('Wybor: '))
            if choice == 0:
                break
            elif choice == 4:
                self.choose_devices()

    def choose_devices(self):
        all_devices = utils.get_devices()
        while True:
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
            print('')
            print('0. Powrot')
            print('--------------------')
            choice = input('Wybor: ')
            if choice == 'a':
                all_devices = utils.get_devices()
                continue
            choice = int(choice)
            if choice == 0:
                break
            elif 0 < choice <= len(all_devices):
                choice -= 1
                if all_devices[choice] in self.devices:
                    self.devices.remove(all_devices[choice])
                else:
                    self.devices.append(all_devices[choice])
