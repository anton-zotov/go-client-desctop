from tkinter import *


class Scene():
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.frame.update()

    def destroy(self):
    	self.frame.destroy()
