from tkinter import Toplevel
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import filedialog
import tkinter as tk


class NewProjectWindow:

    def __init__(self, parent, model):
        self.model = model
        self.parent = parent
        self.window = Toplevel(parent.window)
        self.window.title('Nowy projekt')
        self.window.geometry('600x90')
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.columnconfigure(1, weight=1)
        Label(self.window, text='Nazwa projektu:').grid(row=0, sticky=tk.NW+tk.N+tk.S)
        self.name_entry = Entry(self.window)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky=tk.NW+tk.N+tk.S+tk.E)
        Label(self.window, text='Ścieżka do projektu:').grid(row=1, column=0, sticky=tk.NW+tk.N+tk.S)
        self.path_label = Label(self.window, anchor=tk.W, bg='white', width=40)
        self.path_label.grid(row=1, column=1, sticky=tk.NW+tk.N+tk.S+tk.E)
        Button(self.window, text='Wybierz', command=self.pick_dir).grid(row=1, column=2, sticky=tk.NW+tk.N+tk.S)
        Button(self.window, text='Anuluj', command=self.destroy).grid(row=2, column=0, sticky=tk.NW + tk.N + tk.S+tk.E)
        Button(self.window, text='Stwórz', command=self.create).grid(row=2, column=2, sticky=tk.NW + tk.N + tk.S+tk.E)

    def pick_dir(self):
        options = {}
        options['defaultextension'] = '.afz'
        options['filetypes'] = [('Pliki projektu', '.afz'), ('Wszystkie pliki', '.*')]
        options['title'] = 'Utwórz projekt'
        filename = filedialog.asksaveasfilename(**options)
        self.path_label.config(text=filename)

    def create(self):
        self.model.new_project(self.path_label['text'], self.name_entry.get())
        self.parent.init()
        self.destroy()

    def destroy(self):
        self.window.destroy()
