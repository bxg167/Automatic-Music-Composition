from tkinter import *


class ProgressBar:
    def __init__(self, master):
        progressbar_background = Frame(master, bg="Grey")

        self.progressbar = progressbar_background

        self.bar = Frame(progressbar_background, bg="green", width=0, height=20)

        self.bar.pack(anchor=W, side=TOP)
        progressbar_background.pack(fill=X, expand=YES)


    def set_percentage(self, percentage):
        if 0 <= percentage <= 100:
            self.bar.configure(width=percentage / 100 * self.progressbar.winfo_width())
        self.progressbar.update()
