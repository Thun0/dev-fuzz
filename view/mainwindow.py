from view.newprojectwindow import NewProjectWindow
from view.driverswindow import DriversWindow
from view.progresswindow import ProgressWindow
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
from tkinter import Radiobutton
from tkinter import Entry


class MainWindow:

    devices_lb = None

    def __init__(self, model):
        width = 800
        height = 600
        self.log_txt = None
        self.start_btn = None
        self.end_count_entry = None
        self.end_hour_entry = None
        self.end_minute_entry = None
        self.devpath_label = None
        self.model = model
        self.window = tk.Tk()
        self.data_source = IntVar()
        self.end_cause = IntVar()
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

        corpus_menu = tk.Menu(menubar, tearoff=0)
        corpus_menu.add_command(label="Dodaj")

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Ogólne")
        settings_menu.add_command(label="Mutator")

        menubar.add_cascade(label="Projekt", menu=project_menu)
        menubar.add_cascade(label="Korpus", menu=corpus_menu)
        menubar.add_cascade(label="Generator")
        menubar.add_cascade(label="Ustawienia", menu=settings_menu)
        menubar.add_cascade(label="Pomoc")

        self.window.config(menu=menubar)
        #self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=2)
        self.window.rowconfigure(1, weight=1)
        self.init()

    def init(self):
        if self.model.project is not None:
            self.initialize_window()

    def initialize_window(self):
        project_frame = Frame(self.window)
        log_frame = Frame(self.window, relief=tk.SUNKEN)
        project_frame.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        log_frame.grid(row=1, column=0, columnspan=5, sticky=tk.N+tk.E+tk.S+tk.W, padx=5, pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=1)
        self.initialize_project_frame(project_frame)
        self.initialize_log_frame(log_frame)
        devices_frame = Frame(self.window)
        devices_frame.columnconfigure(0, weight=1)
        devices_frame.rowconfigure(1, weight=1)
        self.initialize_devices_frame(devices_frame)
        devices_frame.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W, padx=10)

    def refresh_device_list(self):
        pass

    def initialize_project_frame(self, project_frame):
        Label(project_frame, text='Projekt: {}'.format(self.model.project.name), font='Helvetica 16 bold').grid(sticky=tk.NW, columnspan=4, pady=10)
        self.devpath_label = Label(project_frame, text='Sterownik: {}'.format(self.model.project.devpath))
        self.devpath_label.grid(row=1, columnspan=4, sticky=tk.NW, pady=20)
        Button(project_frame, text='Wybierz', command=self.list_drivers).grid(row=1, column=5, sticky=tk.NE, pady=13, padx=5)
        Label(project_frame, text='Korpus: {}'.format(self.model.project.corpuspath)).grid(row=2, columnspan=4, sticky=tk.NW, pady=5)
        Button(project_frame, text='Wybierz').grid(row=2, column=5, sticky=tk.NE, padx=5)
        Label(project_frame, text='Źródło danych', font=self.pane_title_font).grid(row=3, column=0, sticky=tk.NW, pady=10)
        Radiobutton(project_frame, text='Korpus', variable=self.data_source, value=0).grid(row=4, column=0, sticky=tk.NW)
        Radiobutton(project_frame, text='Generator', variable=self.data_source, value=1).grid(row=5, column=0, sticky=tk.NW)
        methods_frame = Frame(project_frame)
        self.initialize_methods_frame(methods_frame)
        methods_frame.grid(row=6, column=0, sticky=tk.NW, pady=10)
        Label(project_frame, text='Warunek zakończenia testu', font=self.pane_title_font).grid(row=7, column=0, sticky=tk.NW)
        Radiobutton(project_frame, text='Brak', variable=self.end_cause, value=0).grid(row=8, column=0,
                                                                                       sticky=tk.NW)
        Radiobutton(project_frame, text='Czas', variable=self.end_cause, value=1).grid(row=9, column=0,
                                                                                           sticky=tk.NW)
        self.end_hour_entry = Entry(project_frame, width=2)
        self.end_hour_entry.grid(row=9, column=1, sticky=tk.NW)
        Label(project_frame, text='h').grid(row=9, column=2, sticky=tk.NW)
        self.end_minute_entry = Entry(project_frame, width=2)
        self.end_minute_entry.grid(row=9, column=3, sticky=tk.NW)
        self.end_hour_entry.insert(tk.END, '0')
        self.end_minute_entry.insert(tk.END, '0')
        Label(project_frame, text='m').grid(row=9, column=4, sticky=tk.NW)
        Radiobutton(project_frame, text='Liczba wywołań', variable=self.end_cause, value=2).grid(row=10, column=0,
                                                                                              sticky=tk.NW)
        self.end_count_entry = Entry(project_frame)
        self.end_count_entry.insert(tk.END, '100000')
        self.end_count_entry.grid(row=10, column=1, columnspan=4, sticky=tk.NW)
        self.start_btn = Button(project_frame, text='Start', command=self.start_run)
        self.start_btn.grid(row=11, pady=20, padx=10, sticky=tk.NE)
        Button(project_frame, text='Restart').grid(row=11, column=1, columnspan=4, pady=20, sticky=tk.NW)

    def initialize_log_frame(self, log_frame):
        Label(log_frame, text='Log').grid(sticky=tk.NW)
        self.log_txt = Text(log_frame, height=5, width=60, wrap=tk.WORD)
        self.log_txt.config(state=tk.DISABLED)
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

    def refresh_driver(self):
        self.devpath_label.config(text='Sterownik: {}'.format(self.model.project.devpath))

    def run(self):
        self.window.mainloop()

    def log(self, txt):
        self.log_txt.config(state=tk.NORMAL)
        self.log_txt.insert(tk.END, txt)
        self.log_txt.config(state=tk.DISABLED)

    def start_run(self):
        self.log('Starting testing process..\n')
        self.model.start_run()

    def load_project_file(self):
        options = {}
        options['defaultextension'] = '.afz'
        options['filetypes'] = [('Pliki projektu', '.afz'), ('Wszystkie pliki', '.*')]
        options['title'] = 'Załaduj projekt'
        filename = filedialog.askopenfilename(**options)
        if filename is not ():
            self.model.load_project(filename)

    def new_project(self):
        NewProjectWindow(self, self.model)

    def list_drivers(self):
        DriversWindow(self, self.model)

    def save_project_file(self):
        if self.model is not None:
            self.model.save_project(self.model.project.filepath)

    def save_project_file_as(self):
        if self.model is not None:
            options = {}
            options['defaultextension'] = '.afz'
            options['filetypes'] = [('Pliki projektu', '.afz'), ('Wszystkie pliki', '.*')]
            options['title'] = 'Zapisz projekt jako..'
            filename = filedialog.asksaveasfilename(**options)
            self.model.save_project(filename)
