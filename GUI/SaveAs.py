from Tkinter import *
import os

from GUI.FolderBrowser import FolderBrowser
from GUI.PopUp import PopUp


class SaveAs(FolderBrowser):
    def __init__(self):
        FolderBrowser.__init__(self)

        self.file_name_entry = Entry(self)
        self.file_name_entry.pack(side=LEFT, padx=5, fill=X)

    def add_button(self):
        select_button = Button(self, text="Save", width=8, command=self.make_selection)
        select_button.pack(side=RIGHT, padx=5, pady=5)

    def make_selection(self):
        file_name = self.file_name_entry.get()
        if file_name != "":
            if not file_name.endswith(".mid"):
                file_name += ".mid"

            print file_name
            self.selection = os.path.abspath(os.path.join(self.working_directory, file_name))
            self.destroy()
        else:
            PopUp("Please enter a file name")

    def explore_folder(self, event):
        temp_name = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
        if os.path.isdir(temp_name):
            self.working_directory = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
            self.fill(self.working_directory)
            self.reset_selection()
