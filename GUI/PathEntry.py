from Tkinter import *

from FolderBrowser import FolderBrowser


class PathEntry(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        button = Button(self, text="Browse", padx=10, command=self.open_explorer)
        button.pack(side=RIGHT)

        self.field = Entry(self)
        self.field.pack(fill=X, padx=5, expand=YES, side=RIGHT)

    def open_explorer(self):
        browser = FolderBrowser()
        browser.grab_set()
        browser.wait_window()
        print(browser.chosen_directory)
        print("done")
        if browser.chosen_directory != "":
            self.field.delete(0, END)
            self.field.insert(0, browser.chosen_directory)
