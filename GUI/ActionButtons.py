from tkinter import *


class ActionButtons(Frame):
    def __init__(self, master, run=0, stop=0):
        Frame.__init__(self, master)

        self.isRunning = False

        self.startButton = Button(self, text="Start", width=6)
        self.cancelButton = Button(self, text="Cancel", width=6)

        self.cancelButton.pack(side=RIGHT, padx=5, pady=5)
        self.startButton.pack(side=RIGHT, padx=5, pady=5)

        self.configure(run=run, stop=stop)
        self.set_not_running()

    def configure(self, run=0, stop=0):
        if run != 0:
            self.startButton.configure(command=run)
        if stop != 0:
            self.cancelButton.configure(command=stop)

    def set_running(self):
        self.startButton.configure(state=DISABLED)
        self.cancelButton.configure(state=NORMAL)
        self.isRunning = True
        self.update()

    def set_not_running(self):
        self.startButton.configure(state=NORMAL)
        self.cancelButton.configure(state=DISABLED)
        self.isRunning = False
        self.update()

    def is_running(self):
        return self.isRunning
