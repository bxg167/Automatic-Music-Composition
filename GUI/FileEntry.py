from Tkinter import *

from GUI.FileBrowser import FileBrowser


class FileEntry(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        button = Button(self, text="Browse", padx=10, command=self.open_explorer)
        button.pack(side=RIGHT)

        self.field = Entry(self)
        self.field.pack(fill=X, padx=5, expand=YES, side=RIGHT)

    def open_explorer(self):
        browser = FileBrowser("rcff")
        browser.grab_set()
        browser.wait_window()
        if browser.chosen_file != "":
            self.field.delete(0, END)
            self.field.insert(0, browser.chosen_file)
