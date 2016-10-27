from Queue import Queue
from Tkinter import *
from ActionButtons import ActionButtons
from PopUp import PopUp
from ProgressBar import ProgressBar
from PathEntry import PathEntry

import time
import os

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
        pop_up.grab_set()
        pop_up.mainloop()
        return

    action_buttons.set_running()

    file_queue = Queue(False)
    for name in os.listdir(folder_dir):
        path = os.path.join(folder_dir, name)
        if os.path.isfile(path) and name.endswith(".midi"):
            print(name)
            file_queue.put(name)

    i = 0
    max_size = file_queue.qsize()
    while action_buttons.is_running and max_size > i:
        label.config(text="Current File: " + file_queue.get(False))
        progress_bar.set_percentage(i / float(max_size + 1))
        i += 1
        time.sleep(1)
    if action_buttons.is_running:
        progress_bar.set_percentage(1)
        label.config(text="Finished")
    action_buttons.set_not_running()


def stop():
    action_buttons.set_not_running()
    label.configure(text="Cancelled")

action_buttons.configure(run=run, stop=stop)

window.mainloop()
