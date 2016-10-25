from tkinter import *


class PopUp(Toplevel):
    def __init__(self, text):
        Toplevel.__init__(self)
        self.resizable(width=FALSE, height=FALSE)
        self.minsize(width=180, height=80)

        label = Label(self, text=text, justify=CENTER, height=4)
        label.pack(fill=X)

        button = Button(self, text="Ok", command=self.destroy, padx=10)
        button.pack(pady=5)

        self.focus_force()
