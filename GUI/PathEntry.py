from tkinter import *


class PathEntry(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        button = Button(self, text="Browse", padx=10)
        button.pack(side=RIGHT)

        field = Entry(self)
        field.pack(fill=X, padx=5, expand=YES, side=RIGHT)
