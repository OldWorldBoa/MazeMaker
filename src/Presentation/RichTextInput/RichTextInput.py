from tkinter import Frame, Text, BOTH

from .RichTextInputMenu import RichTextInputMenu


class RichTextInput(Frame):
    def __init__(self, master):
        super().__init__(master, bg="gray75")

        self.menu = RichTextInputMenu(self)
        self.input = Text(self, height=15)

    def display(self, **kwargs):
        super().grid(kwargs)

        self.menu.display()
        self.input.pack(fill=BOTH)
