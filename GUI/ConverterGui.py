from Queue import Queue
from Tkinter import *

from ActionButtons import ActionButtons
from GUI import Mediator
from GUI.Mediator import Mediator
from PopUp import PopUp
from ProgressBar import ProgressBar
from PathEntry import PathEntry

import os
import sys

CURRENT_DIRECTORY = os.path.dirname(__file__)
sys.path.append(CURRENT_DIRECTORY + "..")
sys.path.append(CURRENT_DIRECTORY)
print CURRENT_DIRECTORY

import pip


def install():
    pip.main(['install', 'python-midi'])

MIN_HEIGHT = 125
MIN_WIDTH = 260

window = Tk()

window.geometry("440x" + str(MIN_HEIGHT))
window.minsize(width=MIN_WIDTH, height=MIN_HEIGHT)
window.resizable(width=TRUE, height=FALSE)

path_entry = PathEntry(window)

label = Label(path_entry, text="Folder")
label.pack(side=LEFT)

path_entry.pack(fill=X, expand=YES, padx=10, pady=10)

label = Label(window)
label.pack(padx=10, anchor=W)

progress_bar = ProgressBar(window)
progress_bar.pack(fill=X, expand=YES, padx=10)

action_buttons = ActionButtons(window)
action_buttons.pack(fill=X, padx=5)


def run():
    folder_dir = path_entry.field.get()
    if not os.path.isdir(folder_dir):
        pop_up = PopUp("Not a valid directory")
        return

    action_buttons.set_running()

    file_queue = Queue(False)
    folder_queue = Queue(False)
    folder_queue.put(folder_dir)

    while not folder_queue.empty():
        folder = folder_queue.get()
        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            if os.path.isfile(path) and name.endswith(".mid"):
                file_queue.put(path)
            elif os.path.isdir(path):
                folder_queue.put(path)

    i = 0
    max_size = file_queue.qsize()

    if max_size == 0:
        p = PopUp("There are no midis in this folder.")
        action_buttons.set_not_running()

    isError = False
    while action_buttons.is_running and max_size > i:
        file_path = file_queue.get(False)
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        label.config(text="Current File: " + file_name)
        progress_bar.set_percentage(i / float(max_size + 1))
        i += 1

        if Mediator.convert_file(file_name, file_dir) == TypeError:
            isError = True

    if action_buttons.is_running:
        progress_bar.set_percentage(1)

        if not isError:
            label.config(text="Finished.")
        else:
            label.config(text="Finished With Errors.")

    action_buttons.set_not_running()


def stop():
    action_buttons.set_not_running()
    label.configure(text="Cancelled")
    p = PopUp("Cancelled")

action_buttons.configure(run=run, stop=stop)

window.mainloop()
