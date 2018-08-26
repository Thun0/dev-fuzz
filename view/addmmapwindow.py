from tkinter import Toplevel
from tkinter import Button
from tkinter import Listbox
from tkinter import Scrollbar
import tkinter as tk
import threading
from view.progresswindow import ProgressWindow


class AddMmapWindow:

    def __init__(self, parent, model):
        self.model = model
        self.parent = parent
        self.window = Toplevel(parent.window)
        self.window.title('Lista sterowników')
        self.window.geometry('600x400')
        Button(self.window, text='Dodaj', command=self.add_case).grid()
        self.window.transient(master=parent.window)
        self.window.grab_set()

    def add_case(self):
        pass

    def destroy(self):
        self.window.grab_release()
        self.window.destroy()