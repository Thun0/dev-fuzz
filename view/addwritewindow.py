from tkinter import Toplevel
from tkinter import Button
from tkinter import Entry
from tkinter import Text
from tkinter import Label
from tkinter import Radiobutton
from tkinter import messagebox
import struct
import tkinter as tk


class AddWriteWindow:

    def __init__(self, parent, model):
        self.buf_type = tk.IntVar()
        self.model = model
        self.parent = parent
        self.window = Toplevel(parent.window)
        self.window.title('Dodaj test write')
        self.window.geometry('300x320')
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(4, weight=1)
        Label(self.window, text='Parametr count').grid(sticky=tk.NW)
        self.count_entry = Entry(self.window)
        self.count_entry.grid(row=0, column=1, sticky=tk.NW)
        Radiobutton(self.window, text='Bufor znakowy', variable=self.buf_type, value=0).grid(row=2, column=0,
                                                                                       sticky=tk.NW)
        Radiobutton(self.window, text='Bufor bajtów (hex)', variable=self.buf_type, value=1).grid(row=2, column=1,
                                                                                       sticky=tk.NW)
        Label(self.window, text='Zawartość bufora').grid(row=3, sticky=tk.NW)
        self.buffer_entry = Text(self.window, width=36, height=12)
        self.buffer_entry.grid(row=4, columnspan=3, sticky=tk.NW+tk.E+tk.S, padx=5)
        Button(self.window, text='Dodaj', command=self.add_case).grid(row=5, columnspan=2)
        self.window.transient(master=parent.window)
        self.window.grab_set()

    def add_case(self):
        text = self.buffer_entry.get("1.0", tk.END).strip()
        try:
            if self.buf_type.get() == 0:
                self.model.corpus.add_case(struct.pack('Q{}s'.format(len(text.encode())), int(self.count_entry.get()), text.encode()), 'write')
            else:
                print(str(text))
                buf_bytes = bytes.fromhex(str(text))
                print(buf_bytes)
                self.model.corpus.add_case(struct.pack('Q{}s'.format(len(buf_bytes)), int(self.count_entry.get()), buf_bytes), 'write')
            self.destroy()
        except ValueError:
            messagebox.showinfo("Błąd", "Podano złą wartość argumentu")

    def destroy(self):
        self.window.grab_release()
        self.window.destroy()
