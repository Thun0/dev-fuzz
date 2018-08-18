from pathlib import Path
import settings
from project import Project
from view.mainwindow import MainWindow
from model import Model


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
        # TODO: filter to remove path traversal
        project_name = input('Podaj nazwe projektu: ')
        p = Path().absolute().parents[0]
        p /= settings.config['projects_dir']
        p /= (project_name+'.afz')
        if p.exists():
            print('Projekt o podanej nazwie juz istnieje!')
        else:
            project = Project(project_name)
            project.create(p)
            settings.config['project'] = project
            print('Stworzono projekt: {}'.format(p))
            project.main_menu()
            break


def load_project():
    while True:
        project_name = input('Podaj nazwe lub sciezke projektu (0 - powrót do menu): ')
        try:
            if int(project_name) == 0:
                break
        except ValueError:
            pass
        if Path(project_name).exists():
            project = Project(project_name.split('/')[-1])
            project.load(project_name)
        p = Path().absolute().parents[0]
        p /= settings.config['projects_dir']
        p /= (project_name + '.afz')
        if p.exists():
            project = Project(project_name)
            project.load(p)
        else:
            print('Projekt o podanej nazwie/sciezce nie istnieje!')
            continue
        project.main_menu()
        break


if __name__ == "__main__":
    model = Model()
    main_window = MainWindow(model)
    model.view = main_window
    main_window.run()
