from Tkinter import *


class ProgressBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.progress_bar = Frame(self, bg="Grey", relief=SUNKEN)

        self.bar = Frame(self.progress_bar, bg="green", width=0, height=20)

        self.bar.pack(anchor=W, side=TOP)
        self.progress_bar.pack(fill=X, expand=YES)

    def set_percentage(self, percentage):
        if 0 <= percentage <= 1:
            self.bar.configure(width=percentage * self.progress_bar.winfo_width())
        self.progress_bar.update()
        self.update()
        self.master.update()

        self.bar.update()
