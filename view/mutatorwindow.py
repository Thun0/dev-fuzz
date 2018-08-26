from tkinter import Toplevel
from tkinter import Button
from tkinter import Checkbutton
from tkinter import Label
import tkinter as tk


class MutatorWindow:

    def __init__(self, parent, model):
        self.model = model
        self.parent = parent
        self.window = Toplevel(parent.window)
        self.mutations = self.model.get_mutations()
        self.window.title('Mutator')
        self.window.geometry('600x400')
        self.window.transient(master=parent.window)
        self.window.grab_set()
        Label(self.window, text='Wybrane mutacje').grid(sticky=tk.NW)
        for i in range(0, len(self.mutations)):
            Checkbutton(self.window, text=self.mutations[i][0], variable=self.mutations[i][1]).grid(row=i+1,
                                                                                                        sticky=tk.NW)

    def destroy(self):
        self.window.grab_release()
        self.window.destroy()
