from Tkinter import *

import errno

from GUI.FileEntry import FileEntry
from PopUp import PopUp

import os

MIN_HEIGHT = 125
MIN_WIDTH = 260

window = Tk()

window.geometry("440x" + str(MIN_HEIGHT))
window.minsize(width=MIN_WIDTH, height=MIN_HEIGHT)
window.resizable(width=TRUE, height=FALSE)

path_entry = FileEntry(window)

label = Label(path_entry, text="RNN Snapshot")
label.pack(side=LEFT)

path_entry.pack(fill=X, expand=YES, padx=10, pady=10)

created_text = Label(window)
created_text.pack(fill=X)

start_button = Button(window, text="Start", width=6)
start_button.pack(padx=5, pady=5)


def run():
    folder_dir = path_entry.field.get()
    if not os.path.isfile(folder_dir):
        pop_up = PopUp("Not a valid file")
        pop_up.grab_set()
        pop_up.mainloop()
        return

    print "Hello, This is where the code is supposed to go."
    created_text.configure(text="Successfully Completed.")

start_button.configure(command=run)

window.mainloop()
