from tkinter import Toplevel
from tkinter import Button
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import Entry
from tkinter import Text
from tkinter import Label
from tkinter import messagebox
import struct


class AddIoctlWindow:

    types = ['ciąg bajtów (hex)', 'ciąg znaków', 'int (2 bajty)', 'int (4 bajty)',
             'int (8 bajtów)', 'float (4 bajty)', 'double (8 bajtów)']

    def __init__(self, parent, model):
        self.args = []
        self.format = ''
        self.model = model
        self.parent = parent
        self.window = Toplevel(parent.window)
        self.window.title('Dodaj test ioctl')
        self.window.geometry('375x320')
        self.type = tk.StringVar()
        Label(self.window, text='Kod metody ioctl').grid(row=0, column=0, sticky=tk.NW)
        self.cmd_code_entry = Entry(self.window)
        self.cmd_code_entry.grid(column=1, row=0, sticky=tk.NW)
        Label(self.window, text='Dodaj argument').grid(row=2, sticky=tk.NW)
        Label(self.window, text='Typ').grid(row=3, sticky=tk.NW)
        Button(self.window, text='Dodaj', command=self.add_argument).grid(row=3, column=2, rowspan=2)
        self.combobox = Combobox(self.window, textvariable=self.type,
                                 values=self.types)
        self.arg_entry = Entry(self.window)
        self.combobox.grid(row=3, column=1, sticky=tk.NW)
        Label(self.window, text='Wartość').grid(row=4, sticky=tk.NW)
        self.arg_entry.grid(row=4, column=1, sticky=tk.NW)
        Label(self.window, text='Przypadek testowy').grid(row=5, sticky=tk.NW)
        self.args_text = Text(self.window, width=36, wrap=tk.CHAR, height=10)
        self.args_text.grid(row=6, columnspan=5, sticky=tk.NW+tk.S+tk.E)
        Button(self.window, text='Dodaj', command=self.add_case).grid(row=7, column=2)
        self.window.transient(master=parent.window)
        self.window.grab_set()

    def add_argument(self):
        idx = -1
        type = str(self.type.get())
        for i in range(0, len(self.types)):
            if self.types[i] == type:
                idx = i
        if idx == -1:
            messagebox.showinfo("Błąd", "Brak podanego typu argumentu")

        try:
            if idx == 0:
                self.format += '{}s'.format(int(len(self.arg_entry.get())/2))
                self.args.append(bytes.fromhex(str(self.arg_entry.get())))
                self.args_text.insert(tk.END, '#')
            elif idx == 1:
                self.format += '{}s'.format(len(self.arg_entry.get()))
                self.args.append(str(self.arg_entry.get()).encode())
            elif idx == 2:
                self.format += 'h'
                self.args.append(int(self.arg_entry.get()))
            elif idx == 3:
                self.format += 'i'
                self.args.append(int(self.arg_entry.get()))
            elif idx == 4:
                self.format += 'q'
                self.args.append(int(self.arg_entry.get()))
            elif idx == 5:
                self.format += 'f'
                self.args.append(float(self.arg_entry.get()))
            elif idx == 6:
                self.format += 'd'
                self.args.append(float(self.arg_entry.get()))
            else:
                return
        except ValueError:
            messagebox.showinfo("Błąd", "Podano złą wartość argumentu")
        self.args_text.insert(tk.END, '{}\n'.format(self.arg_entry.get()))
        self.arg_entry.config(text='')

    def destroy(self):
        self.window.grab_release()
        self.window.destroy()

    def add_case(self):
        print('Format: q{}'.format(self.format))
        if self.cmd_code_entry.get() == '':
            messagebox.showinfo("Błąd", "Podaj kod metody")
            return
        try:
            code = int(self.cmd_code_entry.get())
            data = struct.pack('q{}'.format(self.format), code, *self.args)
            self.model.corpus.add_case(data, 'ioctl')
            self.parent.log('Dodano test ioctl\n')
            self.destroy()
        except ValueError:
            messagebox.showinfo("Błąd", "Wartość kodu metody musi być liczbą!")
            return

