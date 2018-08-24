from tkinter.ttk import Progressbar
from tkinter import Toplevel
from tkinter import Label
import tkinter as tk


class ProgressWindow:

    def __init__(self, parent, msg):
        self.parent = parent
        self.msg = msg
        self.window = None

    def start(self):
        self.window = Toplevel(self.parent.window)
        self.window.protocol('WM_DELETE_WINDOW', do_nothing)
        bar = Progressbar(self.window, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        label = Label(self.window, text=self.msg)
        self.window.title('Proszę czekać')
        self.window.geometry('300x50')
        #self.window.lift(aboveThis=self.parent.window)
        self.window.attributes("-topmost", True)
        label.pack(side=tk.TOP)
        bar.pack(side=tk.TOP)
        bar.start(10)
        self.window.grab_set()

    def destroy(self):
        self.window.grab_release()
        self.window.destroy()


def do_nothing():
    pass
