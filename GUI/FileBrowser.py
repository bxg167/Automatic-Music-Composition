from Tkinter import *
import os

from GUI.FolderBrowser import FolderBrowser


class FileBrowser(FolderBrowser):
    def __init__(self, file_extension):
        self.file_type = file_extension

        FolderBrowser.__init__(self)

    def make_selection(self):
        temp_file_name = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
        if os.path.isfile(temp_file_name):
            self.selection = temp_file_name
            self.destroy()
        else:
            self.explore_folder(temp_file_name)

    def explore_folder(self, event):
        temp_name = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
        if os.path.isdir(temp_name):
            self.working_directory = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
            self.fill(self.working_directory)
            self.reset_selection()

    def fill(self, folder_dir):
        self.menu.delete(0, END)

        i = 1
        self.menu.insert(0, "..")
        for name in os.listdir(folder_dir):
            path_name = os.path.join(folder_dir, name)
            if os.path.isdir(path_name):
                self.menu.insert(i, name)
                i += 1
            if os.path.isfile(path_name) and name.endswith(self.file_type):
                self.menu.insert(END, name)
