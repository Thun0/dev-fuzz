from view.newprojectwindow import NewProjectWindow
from android import utils
import tkinter as tk
from tkinter import filedialog
from tkinter import Frame
from tkinter import Label
from tkinter import Checkbutton
from tkinter import IntVar
from tkinter import Listbox
from tkinter import Button
from tkinter import Text


class MainWindow:

    devices_lb = None

    def __init__(self, model):
        width = 800
        height = 600
        self.log_txt = None
        self.model = model
        self.window = tk.Tk()
        self.window.title('ADFuzz')
        self.window.geometry('{}x{}'.format(width, height))
        self.chosen_methods = [IntVar(), IntVar(), IntVar()]
        self.pane_title_font = 'Helvetica 11 bold'
        menubar = tk.Menu(self.window)
        project_menu = tk.Menu(menubar, tearoff=0)
        project_menu.add_command(label="Nowy", command=self.new_project)
        project_menu.add_command(label="Załaduj", command=self.load_project_file)
        project_menu.add_command(label="Zapisz", command=self.save_project_file)
        project_menu.add_command(label="Zapisz jako..", command=self.save_project_file_as)
        menubar.add_cascade(label="Projekt", menu=project_menu)
        menubar.add_cascade(label="Ustawienia")
        menubar.add_cascade(label="Pomoc")
        self.window.config(menu=menubar)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=3)
        self.window.rowconfigure(1, weight=1)
        self.init()

    def init(self):
        if self.model.project is not None:
            self.initialize_left_frame()
            self.initialize_right_frame()

    def initialize_left_frame(self):
        project_frame = Frame(self.window)
        log_frame = Frame(self.window)
        project_frame.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        log_frame.grid(row=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=1)
        self.initialize_project_frame(project_frame)
        self.initialize_log_frame(log_frame)

    def initialize_right_frame(self):
        methods_frame = Frame(self.window)
        devices_frame = Frame(self.window)
        devices_frame.columnconfigure(0, weight=1)
        devices_frame.rowconfigure(1, weight=1)
        self.initialize_methods_frame(methods_frame)
        self.initialize_devices_frame(devices_frame)
        methods_frame.grid(row=0, column=1)
        devices_frame.grid(row=1, column=1, sticky=tk.N+tk.E+tk.S+tk.W)

    def refresh_device_list(self):
        pass

    def initialize_project_frame(self, project_frame):
        Label(project_frame, text='Projekt: {}'.format(self.model.project.name), font='Helvetica 16 bold').grid(sticky=tk.NW)
        Label(project_frame, text='Wybrany sterownik: {}'.format(self.model.project.devpath)).grid(row=1, sticky=tk.NW, pady=20)
        Button(project_frame, text='Wybierz').grid(row=1, column=1, sticky=tk.NW, pady=10)
        Label(project_frame, text='Wybrany korpus: {}'.format(self.model.project.corpuspath)).grid(row=2, sticky=tk.NW)

    def initialize_log_frame(self, log_frame):
        Label(log_frame, text='Log').grid()
        self.log_txt = Text(log_frame, height=5, width=60, wrap=tk.WORD)
        self.log_txt.grid(row=1, sticky=tk.N+tk.E+tk.S+tk.W)

    def initialize_methods_frame(self, methods_frame):
        Label(methods_frame, text='Metody', font=self.pane_title_font).grid(row=0, column=0, sticky=tk.NW)
        Checkbutton(methods_frame, text='ioctl', variable=self.chosen_methods[0]).grid(row=1, column=0, sticky=tk.NW)
        Checkbutton(methods_frame, text='write', variable=self.chosen_methods[1]).grid(row=2, column=0, sticky=tk.NW)
        Checkbutton(methods_frame, text='mmap', variable=self.chosen_methods[2]).grid(row=3, column=0, sticky=tk.NW)

    def initialize_devices_frame(self, devices_frame):
        Label(devices_frame, text='Urządzenia', font=self.pane_title_font).grid(row=0, sticky=tk.NW)
        self.devices_lb = Listbox(devices_frame, height=5)
        for d in utils.get_devices():
            self.devices_lb.insert(tk.END, d.name)
        self.devices_lb.grid(row=1, sticky=tk.N+tk.E+tk.S+tk.W)
        Button(devices_frame, text='Odśwież').grid(row=2)

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
