from tkinter import *


class ActionButtons(Frame):
    def __init__(self, master, run=0, stop=0):
        Frame.__init__(self, master)

        self.is_running = False

        self.start_button = Button(self, text="Start", width=6)
        self.cancel_button = Button(self, text="Cancel", width=6)

        self.cancel_button.pack(side=RIGHT, padx=5, pady=5)
        self.start_button.pack(side=RIGHT, padx=5, pady=5)

        self.configure(run=run, stop=stop)
        self.set_not_running()

    def configure(self, run=0, stop=0):
        if run != 0:
            self.start_button.configure(command=run)
        if stop != 0:
            self.cancel_button.configure(command=stop)

    def set_running(self):
        self.start_button.configure(state=DISABLED)
        self.cancel_button.configure(state=NORMAL)
        self.is_running = True
        self.update()

    def set_not_running(self):
        self.start_button.configure(state=NORMAL)
        self.cancel_button.configure(state=DISABLED)
        self.is_running = False
        self.update()
