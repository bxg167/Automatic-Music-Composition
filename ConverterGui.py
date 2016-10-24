from tkinter import *
import time

from ActionButtons import ActionButtons
from PathEntry import PathEntry
from ProgressBar import ProgressBar

window = Tk()
window.resizable(width=TRUE, height=FALSE)
folderLocation = ""
window.geometry("440x125")

pathEntryFrame = Frame(window)
label = Label(pathEntryFrame, text="Folder")
label.pack(side=LEFT)

PathEntry(pathEntryFrame)
pathEntryFrame.pack(fill=X, expand=YES, padx=10, pady=10)

label = Label(window)
label.pack(padx=10, anchor=W)

progressBarFrame = Frame(window)
progressBar = ProgressBar(progressBarFrame)
progressBarFrame.pack(fill=X, expand=YES, padx=10)

actionButtonsFrame = Frame(window)
actionButtons = ActionButtons(actionButtonsFrame)
actionButtonsFrame.pack(fill=X, padx=5)

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
