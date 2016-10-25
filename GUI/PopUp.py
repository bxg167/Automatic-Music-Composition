from tkinter import *


class PopUp:
    def __init__(self, text):
        popUp = Toplevel()
        popUp.resizable(width=FALSE, height=FALSE)
        popUp.minsize(width=120, height=30)

        label = Label(popUp, text=text)
        label.pack()

        button = Button(popUp, text="Ok", command=popUp.destroy, width=6)
        button.pack()

        popUp.focus_force()

        popUp.wait_window(popUp)
