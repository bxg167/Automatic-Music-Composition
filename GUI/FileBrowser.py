from Tkinter import *
import os


class FileBrowser(Toplevel):
    def __init__(self, file_extension):
        self.file_type = file_extension

        Toplevel.__init__(self)

        self.chosen_file = ""

        menu_frame = Frame(self)
        self.minsize(width=220, height=200)

        self.menu = Listbox(menu_frame, height=10, width=30, selectmode=SINGLE)
        self.scrollbar = Scrollbar(menu_frame, orient=VERTICAL)

        self.menu.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.menu.yview)

        self.menu.bind("<Double-1>", self.explore_folder)
        self.menu.pack(fill=BOTH, expand=YES, side=LEFT)
        self.scrollbar.pack(fill=Y, expand=YES)

        menu_frame.pack(fill=BOTH, expand=YES)

        self.add_button()

        self.working_directory = "."
        self.fill(self.working_directory)

    def add_button(self):
        select_button = Button(self, text="Select", width=8, command=self.make_selection)
        select_button.pack(side=RIGHT, padx=5, pady=5)

    def make_selection(self):
        temp_file_name = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
        if os.path.isfile(temp_file_name):
            self.chosen_file = temp_file_name
            self.destroy()
        else:
            self.explore_folder(temp_file_name)

    def explore_folder(self, event):
        temp_name = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
        if os.path.isdir(temp_name):
            self.working_directory = temp_name
            self.fill(self.working_directory)

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
