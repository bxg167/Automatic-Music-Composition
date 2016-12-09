from Tkinter import *

import midi

from File_Conversion.ConvertRcffToMidi import ConvertRcffToMidi
from File_Conversion.RCFF import RCFF
from GUI.FileEntry import FileEntry
from GUI.SaveAs import SaveAs
from GUI.midi_instruments import *
from PopUp import PopUp

import os

SNAPSHOT_EXTENSION = ".rcff"

MIN_HEIGHT = 125
MIN_WIDTH = 285

window = Tk()

window.geometry("440x" + str(MIN_HEIGHT))
window.minsize(width=MIN_WIDTH, height=MIN_HEIGHT)
window.resizable(width=TRUE, height=FALSE)

# ------------------First Row------------------
first_row = Frame(window)
path_entry = FileEntry(first_row, SNAPSHOT_EXTENSION)


label = Label(path_entry, text="RCFF Files")
label.pack(side=LEFT)

path_entry.pack(fill=X, expand=YES, padx=10, pady=10)

first_row.pack(fill=X, expand=YES)


# ------------------Second Row------------------
second_row = Frame(window)
label = Label(second_row, text="Instrument Selection: ")
spinbox = Spinbox(second_row, from_=0, to=127, values=midi_instrument_list, wrap=True)
label.pack(side=LEFT)
spinbox.pack(side=LEFT)
second_row.pack(fill=X, expand=YES)


#Place holder for actual method
def start_process(midi_file_location):
    status_label.config(text="Composing: " + midi_file_location)

    print path_entry.field.get()
    c = ConvertRcffToMidi(path_entry.field.get())

    # TODO: Send Instrument value.

    instrument_string = spinbox.get()
    midi_object = c.create_midi(midi_instrument_dictionary.get(instrument_string))

    # The midi file should be written from the GUI, just as rcff files are. For now, we'll leave it here
    if not os.path.exists(midi_file_location):
        midi.write_midifile(midi_file_location, midi_object)
        status_label.configure(text=os.path.basename(midi_file_location) + " Successfully Completed.")
    else:
        status_label.configure(text="Error: File already exists")


def open_save_as(starting_folder_dir):
    browser = SaveAs(starting_folder_dir)
    browser.grab_set()
    browser.wait_window()

    if browser.selection != "":
        start_process(browser.selection)
    else:
        status_label.configure(text="Not Completed.")

# ------------------Third Row------------------
third_row = Frame(window)
status_label = Label(window)
status_label.pack()
third_row.pack()

# ------------------Fourth Row------------------
fourth_row = Frame(window)
start_button = Button(fourth_row, text="Start", width=6)

start_button.pack(padx=5, pady=5)
fourth_row.pack()

def run():
    file_dir = path_entry.field.get()

    if not os.path.isfile(file_dir):
        PopUp("Not a valid file")
        return

    folder_dir = os.path.dirname(file_dir)

    open_save_as(folder_dir)

start_button.configure(command=run)

window.mainloop()
