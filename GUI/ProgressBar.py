from tkinter import *


class ProgressBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        progressbar_background = Frame(self, bg="Grey", relief=SUNKEN)

        self.progress_bar = progressbar_background

        self.bar = Frame(progressbar_background, bg="green", width=0, height=20)

        self.bar.pack(anchor=W, side=TOP)
        progressbar_background.pack(fill=X, expand=YES)

    def set_percentage(self, percentage):
        if 0 <= percentage <= 1:
            self.bar.configure(width=percentage * self.progress_bar.winfo_width())
        self.progress_bar.update()
