from Tkinter import *

from GUI.FileEntry import FileEntry
from GUI.SaveAs import SaveAs
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


#Place holder for actual method
def start_process(file_name):
    print "Composing: " + file_name

def open_save_as():
    browser = SaveAs()
    browser.grab_set()
    browser.wait_window()

    if browser.selection != "":
        start_process(browser.selection)
        created_text.configure(text=os.path.basename(browser.selection) + " Successfully Completed.")
    else:
        created_text.configure(text="Not Completed.")


start_button = Button(window, text="Start", width=6)

start_button.pack(padx=5, pady=5)


def run():
    folder_dir = path_entry.field.get()

    if not os.path.isfile(folder_dir):
        PopUp("Not a valid file")
        return

    open_save_as()

start_button.configure(command=run)

window.mainloop()
