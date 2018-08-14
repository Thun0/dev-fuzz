from tkinter import Toplevel


class NewProjectWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.title('Nowy projekt')
        self.window.geometry('400x300')

    def destroy(self):
        self.window.destroy()
