from tkinter import *
import os
import tkinter


class FolderBrowser(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.chosen_directory = ""
        menuframe = Frame(self)
        self.menu = Listbox(menuframe, height=10, width=50, selectmode=tkinter.SINGLE)
        self.scrollbar = Scrollbar(menuframe, orient=VERTICAL)

        self.menu.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.menu.yview)

        self.menu.bind("<Double-1>", self.explore_folder)
        self.menu.pack(fill=BOTH, expand=YES, side=LEFT)
        self.scrollbar.pack(fill=Y, expand=YES)

        menuframe.pack(fill=BOTH, expand=YES)

        button = Button(self, text="Select", width=8, command=self.make_selection)
        button.pack(side=RIGHT, padx=5)

        button = Button(self, text="Browse", width=8)
        button.pack(side=RIGHT, padx=5)
        button.bind("<Button-1>", self.explore_folder)

        self.workingDirectory = "."
        self.fill(self.workingDirectory)

    def make_selection(self):
        self.chosen_directory = os.path.abspath(os.path.join(self.workingDirectory, self.menu.selection_get()))
        self.master.destroy()

    def explore_folder(self, event):
        self.workingDirectory = os.path.abspath(os.path.join(self.workingDirectory, self.menu.selection_get()))
        print(self.workingDirectory)
        self.fill(self.workingDirectory)

    def fill(self, folderDir):
        self.menu.delete(0, END)

        i = 1
        self.menu.insert(0, "..")
        for name in os.listdir(folderDir):
            if os.path.isdir(os.path.join(folderDir, name)):
                self.menu.insert(i, name)
                i += 1
            # Will be used if I decide to make this a folder & file browser (Possibly for an advanced window)
            # if os.path.isfile(os.path.join(dir, name)):
            #     self.menu.insert(tkinter.END, name)
