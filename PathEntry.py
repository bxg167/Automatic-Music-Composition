from tkinter import *


class PathEntry:
    def __init__(self, master):
        button = Button(master, text="Browse", padx=10)
        button.pack(side=RIGHT)

        field = Entry(master)
        field.pack(fill=X, padx=5, expand=YES, side=LEFT)
