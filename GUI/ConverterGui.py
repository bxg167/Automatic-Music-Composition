from tkinter import *
from GUI.ActionButtons import ActionButtons
from GUI.ProgressBar import ProgressBar
from GUI.PathEntry import PathEntry

import time

MIN_HEIGHT = 125
MIN_WIDTH = 260

window = Tk()
window.geometry("440x" + str(MIN_HEIGHT))
window.minsize(width=MIN_WIDTH, height=MIN_HEIGHT)
window.resizable(width=TRUE, height=FALSE)

pathEntry = PathEntry(window)

label = Label(pathEntry, text="Folder")
label.pack(side=LEFT)

pathEntry.pack(fill=X, expand=YES, padx=10, pady=10)

label = Label(window)
label.pack(padx=10, anchor=W)

progressBar = ProgressBar(window)
progressBar.pack(fill=X, expand=YES, padx=10)

actionButtons = ActionButtons(window)
actionButtons.pack(fill=X, padx=5)


def run():
    actionButtons.set_running()

    # Change with file name
    label.configure(text="Running")

    i = 0
    while actionButtons.is_running() and i < 100:
        i += 1
        progressBar.set_percentage(i)
        time.sleep(1 / 10)
    if actionButtons.is_running():
        label.config(text="Finished")
    actionButtons.set_not_running()


def stop():
    actionButtons.set_not_running()
    label.configure(text="Cancelled")

actionButtons.configure(run=run, stop=stop)

window.mainloop()
