import tkinter as tk
from tkinter import filedialog
from view.newprojectwindow import NewProjectWindow
from tkinter import PanedWindow
from tkinter import Label
from tkinter import Checkbutton
from tkinter import IntVar


class MainWindow:
    def __init__(self, model):
        width = 800
        height = 600
        self.model = model
        self.window = tk.Tk()
        self.window.title('ADFuzz')
        self.window.geometry('{}x{}'.format(width, height))
        menubar = tk.Menu(self.window)
        project_menu = tk.Menu(menubar, tearoff=0)
        project_menu.add_command(label="Nowy", command=self.new_project)
        project_menu.add_command(label="Załaduj", command=self.load_project_file)
        project_menu.add_command(label="Zapisz", command=self.save_project_file)
        project_menu.add_command(label="Zapisz jako..", command=self.save_project_file_as)
        menubar.add_cascade(label="Projekt", menu=project_menu)
        menubar.add_cascade(label="Ustawienia")
        menubar.add_cascade(label="Pomoc")
        self.chosen_methods = [IntVar(), IntVar(), IntVar()]
        self.pane_title_font = 'Helvetica 11 bold'

        main_area = PanedWindow(self.window)
        left_pane = PanedWindow(main_area, width=width*2/3, relief=tk.RIDGE, orient=tk.VERTICAL)
        right_pane = PanedWindow(main_area, relief=tk.RIDGE, orient=tk.VERTICAL)

        self.initialize_left_pane(left_pane)
        self.initialize_right_pane(right_pane)
        main_area.add(left_pane)
        main_area.add(right_pane)
        main_area.pack(fill=tk.BOTH, expand=1)
        self.window.config(menu=menubar)

    def initialize_left_pane(self, left_pane):
        left_pane.add(Label(text='Projekt: {}'.format('test'), font='Helvetica 16 bold'))
        self.initialize_main_pane()

    def initialize_right_pane(self, right_pane):
        methods_pane = PanedWindow(right_pane, relief=tk.RIDGE, orient=tk.VERTICAL)
        methods_pane.add(Label(text='Metody', font=self.pane_title_font))
        methods_pane.add(Checkbutton(methods_pane, text='ioctl', variable=self.chosen_methods[0]))
        methods_pane.add(Checkbutton(methods_pane, text='write', variable=self.chosen_methods[1]))
        methods_pane.add(Checkbutton(methods_pane, text='mmap', variable=self.chosen_methods[2]))
        devices_pane = PanedWindow(right_pane, relief=tk.RIDGE)
        right_pane.add(methods_pane)
        right_pane.add(devices_pane)
        devices_pane.add(Label(text='Urządzenia', font=self.pane_title_font))

    def initialize_main_pane(self):
        pass

    def initialize_log_pane(self):
        pass

    def initialize_methods_pane(self):
        pass

    def initialize_devices_pane(self):
        pass

    def run(self):
        self.window.mainloop()

    def load_project_file(self):
        options = {}
        options['defaultextension'] = '.afz'
        options['filetypes'] = [('Pliki projektu', '.afz'), ('Wszystkie pliki', '.*')]
        options['title'] = 'Załaduj projekt'
        filename = filedialog.askopenfilename(**options)
        self.model.load_project(filename)

    def new_project(self):
        new_project_window = NewProjectWindow(self.window)

    def save_project_file(self):
        if self.model.saved:
            self.model.save()
        else:
            self.save_project_file_as()

    def save_project_file_as(self):
        options = {}
        options['defaultextension'] = '.afz'
        options['filetypes'] = [('Pliki projektu', '.afz'), ('Wszystkie pliki', '.*')]
        options['title'] = 'Zapisz projekt jako..'
        filename = filedialog.asksaveasfilename(**options)
        self.model.save_project(filename)
