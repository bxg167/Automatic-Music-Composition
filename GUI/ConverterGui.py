from Queue import Queue
from Tkinter import *

import errno

from ActionButtons import ActionButtons
from PopUp import PopUp
from ProgressBar import ProgressBar
from PathEntry import PathEntry

import os
import sys

CURRENT_DIRECTORY = os.path.dirname(__file__)
sys.path.append(CURRENT_DIRECTORY + "..")
sys.path.append(CURRENT_DIRECTORY)
print CURRENT_DIRECTORY

from File_Conversion import Converter

import pip


def install():
    pip.main(['install', 'python-midi'])

install()

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
    for name in os.listdir(folder_dir):
        path = os.path.join(folder_dir, name)
        if os.path.isfile(path) and name.endswith(".mid"):
            file_queue.put(name)

    i = 0
    max_size = file_queue.qsize()

    if max_size == 0:
        p = PopUp("There are no midis in this folder.")
        action_buttons.set_not_running()

    isError = False
    while action_buttons.is_running and max_size > i:
        file_name = file_queue.get(False)
        label.config(text="Current File: " + file_name)
        progress_bar.set_percentage(i / float(max_size + 1))
        i += 1

        if convert_file(file_name, folder_dir) == TypeError:
            isError = True

    if action_buttons.is_running:
        progress_bar.set_percentage(1)

        if not isError:
            label.config(text="Finished.")
        else:
            label.config(text="Finished With Errors.")

    action_buttons.set_not_running()


def convert_file(file_name, folder_dir):
    try:
        c = Converter.Converter(os.path.join(folder_dir, file_name))
        rcff_files = c.create_rcff_files()
    except TypeError:
        return TypeError


    i = 0

    new_folder_dir = os.path.join(folder_dir, "RCFF_Files")
    try_create_dir(new_folder_dir)

    for rcff_file in rcff_files:
        new_file_name = os.path.splitext(file_name)[0] + "_" + str(i) + ".rcff"

        file_handler = open(os.path.join(new_folder_dir, new_file_name), "w")

        rcff_file.pickle(file_handler)

        file_handler.close()
        i += 1
    return NoneType

def try_create_dir(new_dir):
    try:
        os.makedirs(new_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def stop():
    action_buttons.set_not_running()
    label.configure(text="Cancelled")
    p = PopUp("Cancelled")

action_buttons.configure(run=run, stop=stop)

window.mainloop()
