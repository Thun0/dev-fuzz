import tkinter as tk
from tkinter import filedialog
from view.newprojectwindow import NewProjectWindow
from tkinter import PanedWindow
from tkinter import Label


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


        left_pane_options = {}
        left_pane_options['width'] = width*2/3
        left_pane_options['relief'] = tk.RIDGE

        default_pane_options = {}
        default_pane_options['relief'] = tk.RIDGE

        main_area = PanedWindow(self.window, **default_pane_options)
        left_pane = PanedWindow(main_area, **left_pane_options, orient=tk.VERTICAL)
        right_pane = PanedWindow(main_area, **default_pane_options, orient=tk.VERTICAL)
        methods_pane = PanedWindow(right_pane, **default_pane_options)
        devices_pane = PanedWindow(right_pane, **default_pane_options)
        right_pane.add(methods_pane)
        right_pane.add(devices_pane)
        main_area.add(left_pane)
        main_area.add(right_pane)
        main_area.pack(fill=tk.BOTH, expand=1)


        left_pane.add(Label(text='1'))
        methods_pane.add(Label(text='2'))
        devices_pane.add(Label(text='3'))

        self.window.config(menu=menubar)

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
