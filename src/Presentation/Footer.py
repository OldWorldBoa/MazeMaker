from tkinter import Frame, X

from .FpsIndicator import FpsIndicator


class Footer(Frame):
    def __init__(self, master):
        super().__init__(master, bg="grey")

        self.master = master
        self.fpsIndicator = FpsIndicator(self)

    def display(self):
        super().pack(expand=False, fill=X, pady=(5, 0))

        self.fpsIndicator.display()
