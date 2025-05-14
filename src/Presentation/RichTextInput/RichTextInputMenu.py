from tkinter import Frame, LEFT, X
from pyeventbus3.pyeventbus3 import *

from src.Presentation.StyledTkinter import StyledTkinter


class RichTextInputMenu(Frame):
    def __init__(self, master):
        super().__init__(master, bg="grey75")

        self.master = master
        self.buttons = []
        self.init_buttons()

    def init_buttons(self):
        self.add_button("Symbols", self.click_save)
        self.add_button("Functions", self.click_save)
        self.add_button("Set Image", self.click_save)

    def add_button(self, text, command):
        self.buttons.append(StyledTkinter.get_styled_button(self, text=text, command=command))

    def display(self):
        super().pack(expand=False, fill=X)

        for button in self.buttons:
            button.pack(side=LEFT, padx=(0, 5), pady=(0, 5))

    def click_save(click_event):
        pass
        # PyBus.Instance().post(SelectToolEvent(SaveTool()))
