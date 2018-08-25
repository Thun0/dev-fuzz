from tkinter import Toplevel
from tkinter import Button
from tkinter import Listbox
from tkinter import Scrollbar
import tkinter as tk
import threading
from view.progresswindow import ProgressWindow


class DriversWindow:

    def __init__(self, parent, model):
        self.model = model
        self.parent = parent
        self.window = Toplevel(parent.window)
        self.window.title('Lista sterowników')
        self.window.geometry('600x400')
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.x_scroll = Scrollbar(self.window, orient=tk.HORIZONTAL)
        self.y_scroll = Scrollbar(self.window, orient=tk.VERTICAL)
        self.x_scroll.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.y_scroll.grid(row=0, column=2, sticky=tk.N + tk.S)
        self.listbox = Listbox(self.window, xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)
        self.x_scroll['command'] = self.listbox.xview
        self.y_scroll['command'] = self.listbox.yview
        threading.Thread(target=self.populate_list).start()
        self.prog_window = ProgressWindow(self, 'Trwa szukanie sterowników')
        self.prog_window.start()
        self.listbox.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W, columnspan=2)
        Button(self.window, text='Wybierz', command=self.pick_dev).grid(row=2, sticky=tk.NE, padx=10)
        Button(self.window, text='Anuluj', command=self.destroy).grid(row=2, column=1, sticky=tk.NW, padx=10)

    def pick_dev(self):
        self.model.project.devpath = self.listbox.get(self.listbox.curselection()).split()[-1]
        self.parent.refresh_driver()
        self.destroy()

    def populate_list(self):
        dev_list = self.model.list_dev_paths()
        for d in dev_list:
            if d is not '':
                self.listbox.insert(tk.END, d)
        self.prog_window.destroy()
        self.window.grab_set()

    def destroy(self):
        self.window.grab_release()
        self.window.destroy()
