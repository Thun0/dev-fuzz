from tkinter import Toplevel
from tkinter import Button
from tkinter import Checkbutton
from tkinter import Label
from tkinter.ttk import Notebook
from tkinter.ttk import Frame
import tkinter as tk


class GeneratorWindow:

    def __init__(self, parent, model):
        self.model = model
        self.parent = parent
        self.window = Toplevel(parent.window)
        self.window.title('Generator')
        self.window.geometry('600x400')
        self.window.transient(master=parent.window)
        self.tabs = Notebook(self.window)
        self.ioctl_frame = Frame(self.tabs)
        self.write_frame = Frame(self.tabs)
        self.mmap_frame = Frame(self.tabs)
        self.tabs.add(self.ioctl_frame, text='ioctl')
        self.tabs.add(self.write_frame, text='write')
        self.tabs.add(self.mmap_frame, text='mmap')
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.tabs.grid(sticky=tk.NW+tk.S+tk.E)
        self.window.grab_set()

    def destroy(self):
        self.window.grab_release()
        self.window.destroy()
