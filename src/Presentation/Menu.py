from tkinter import Frame, LEFT, X

from .StyledTkinter import StyledTkinter


class Menu(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs)

        self.master = master
        self.buttons = []

    def add_button(self, text, command):
        self.buttons.append(StyledTkinter.get_dark_button(self, text=text, command=command))

    def display(self):
        super().pack(expand=False, fill=X)

        for button in self.buttons:
            button.pack(side=LEFT, padx=(0, 5), pady=(0, 5))
