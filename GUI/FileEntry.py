from Tkinter import *

from GUI.FileBrowser import FileBrowser


class FileEntry(Frame):
    def __init__(self, master, file_ext):
        self.file_ext = file_ext
        Frame.__init__(self, master)

        button = Button(self, text="Browse", padx=10, command=self.open_explorer)
        button.pack(side=RIGHT)

        self.field = Entry(self)
        self.field.pack(fill=X, padx=5, expand=YES, side=RIGHT)

    def open_explorer(self):
        browser = FileBrowser(self.file_ext)
        browser.grab_set()
        browser.wait_window()
        if browser.selection != "":
            self.field.delete(0, END)
            self.field.insert(0, browser.selection)
