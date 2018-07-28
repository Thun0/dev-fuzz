from pathlib import Path
import settings
from project import Project


def menu():
    while True:
        print('\033[H\033[J')
        print('Dev-fuzz 0.1')
        print('--------------------')
        print('1. Stworz nowy projekt')
        print('2. Wczytaj projekt')
        print('--------------------')
        print('9. Ustawienia główne')
        print('--------------------')
        print('0. Wyjscie')
        print('--------------------')
        choice = int(input('Wybor: '))
        print(choice)
        if choice == 1:
            create_new_project()
        elif choice == 2:
            load_project()
        elif choice == 9:
            settings_menu()
        elif choice == 0:
            break
        else:
            print('Brak takiej opcji!')
    print(':)')


def settings_menu():
    pass


def create_new_project():
    while True:
        project_name = input('Podaj nazwe projektu: ')
        p = Path().absolute().parents[0]
        p /= settings.config['projects_dir']
        p /= project_name
        p /= '.afz'
        if p.exists():
            print('Projekt o podanej nazwie juz istnieje!')
        else:
            project = Project(project_name)
            settings.config['project'] = project
            print('Stworzono projekt: {}'.format(p))
            project.main_menu()
            break


def load_project():
    pass


if __name__ == "__main__":
    menu()
