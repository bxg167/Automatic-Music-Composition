from tkinter import *
import os
import tkinter

top = Tk()

menu = Listbox(top, height=10, width=50, selectmode=tkinter.SINGLE, yscrollcommand=True)

i = 0
dir = "C:/users/bryce/videos"
for name in os.listdir(dir):
    if os.path.isdir(os.path.join(dir, name)):
        menu.insert(i, name)
        i += 1
    if os.path.isfile(os.path.join(dir, name)):
        menu.insert(tkinter.END, name)

menu.pack()

button = Button(top, text="Select")
button.pack()

top.mainloop()
