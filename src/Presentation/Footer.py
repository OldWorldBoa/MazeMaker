from tkinter import Frame, X

from .FpsIndicator import FpsIndicator
from .StyledTkinter import StyledTkinter


class Footer(Frame):
    def __init__(self, master):
        super().__init__(master, bg=StyledTkinter.get_dark_color())

        self.master = master
        self.fpsIndicator = FpsIndicator(self)

    def display(self):
        super().pack(expand=False, fill=X, pady=(5, 0))

        self.fpsIndicator.display()
