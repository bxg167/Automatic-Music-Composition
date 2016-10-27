from Tkinter import *
import os


class FolderBrowser(Toplevel):
    def __init__(self,):
        Toplevel.__init__(self)

        self.chosen_directory = ""
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

        select_button = Button(self, text="Select", width=8, command=self.make_selection)
        select_button.pack(side=RIGHT, padx=5, pady=5)

        browse_button = Button(self, text="Browse", width=8)
        browse_button.pack(side=RIGHT, padx=5, pady=5)
        browse_button.bind("<Button-1>", self.explore_folder)

        self.working_directory = "."
        self.fill(self.working_directory)

    def make_selection(self):
        self.chosen_directory = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
        self.destroy()

    def explore_folder(self, event):
        self.working_directory = os.path.abspath(os.path.join(self.working_directory, self.menu.selection_get()))
        print(self.working_directory)
        self.fill(self.working_directory)

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
