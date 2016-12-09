import Tkconstants
from Tkinter import *
import os


class FolderBrowser(Toplevel):
    def __init__(self, starting_directory = ".."):
        self.selection_index = -1
        Toplevel.__init__(self)

        self.selection = ""
        first_row = Frame(self, width=440)

        self.directory_label = Label(first_row)
        self.directory_label.pack(pady=5, expand=YES, fill=X)

        first_row.pack(fill=X, expand=YES)

        menu_frame = Frame(self)
        self.minsize(width=440, height=200)

        self.menu = Listbox(menu_frame, height=10, width=30, selectmode=SINGLE)
        self.scrollbar = Scrollbar(menu_frame, orient=VERTICAL)

        self.menu.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.menu.yview)

        self.menu.bind("<Double-1>", self.explore_folder)
        self.menu.bind("<Return>", self.explore_folder)
        self.menu.bind("<Down>", lambda event: self.move_selection(1))
        self.menu.bind("<Up>", lambda event: self.move_selection(-1))
        self.menu.focus_set()

        self.menu.pack(fill=BOTH, expand=YES, side=LEFT)
        self.scrollbar.pack(fill=Y, expand=YES)

        menu_frame.pack(fill=BOTH, expand=YES)

        self.add_button()

        self.working_directory = starting_directory

        self.label_text = StringVar()

        self.label_text.set("Current Directory:\n" + os.path.abspath(self.working_directory))

        self.directory_label.config(textvariable=self.label_text)

        self.reset_selection()

    def move_selection(self, movement):
        self.menu.selection_clear(0, END)

        if 0 <= self.selection_index + movement < self.menu.size():
            self.selection_index = self.selection_index + movement

        if self.selection_index == -1:
            self.selection_index = 0

        self.menu.select_set(first=self.selection_index, last=self.selection_index)

    def add_button(self):
        select_button = Button(self, text="Select", width=8, command=self.make_selection)
        select_button.pack(side=RIGHT, padx=5, pady=5)

    def make_selection(self):
        self.selection = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
        self.destroy()

    def explore_folder(self, event):
        self.working_directory = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
        self.reset_selection()

    def reset_selection(self):
        self.fill(self.working_directory)
        self.label_text.set("Current Directory:\n" + os.path.abspath(self.working_directory))
        self.selection_index = 0
        self.move_selection(0)

    def fill(self, folder_dir):
        self.menu.delete(0, END)

        i = 1
        self.menu.insert(0, "..")
        for name in os.listdir(folder_dir):
            if os.path.isdir(os.path.join(folder_dir, name)):
                self.menu.insert(i, name)
                i += 1
            # Will be used if I decide to make this a folder & file browser (Possibly for an advanced window)
            # if os.path.isfile(os.path.join(dir, name)):
            #     self.menu.insert(tkinter.END, name)
