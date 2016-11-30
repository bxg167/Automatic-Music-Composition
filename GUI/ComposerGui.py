from Tkinter import *

import midi

from File_Conversion.ConvertRcffToMidi import ConvertRcffToMidi
from File_Conversion.RCFF import RCFF
from GUI.FileEntry import FileEntry
from GUI.SaveAs import SaveAs
from PopUp import PopUp

import os

SNAPSHOT_EXTENSION = ".rcff"

MIN_HEIGHT = 125
MIN_WIDTH = 260

window = Tk()

window.geometry("440x" + str(MIN_HEIGHT))
window.minsize(width=MIN_WIDTH, height=MIN_HEIGHT)
window.resizable(width=TRUE, height=FALSE)

path_entry = FileEntry(window, SNAPSHOT_EXTENSION)

label = Label(path_entry, text="RNN Snapshot")
label.pack(side=LEFT)

path_entry.pack(fill=X, expand=YES, padx=10, pady=10)

created_text = Label(window)
created_text.pack(fill=X)


#Place holder for actual method
def start_process(midi_file_location):
    print "Composing: " + midi_file_location
    c = ConvertRcffToMidi(path_entry.field.get())
    midi_object = c.create_midi()

    # The midi file should be written from the GUI, just as rcff files are. For now, we'll leave it here
    if not os.path.exists(midi_file_location):
        midi.write_midifile(midi_file_location, midi_object)
        created_text.configure(text=os.path.basename(midi_file_location) + " Successfully Completed.")
    else:
        created_text.configure(text="Error: File already exists")


def open_save_as():
    browser = SaveAs()
    browser.grab_set()
    browser.wait_window()

    if browser.selection != "":
        start_process(browser.selection)
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
