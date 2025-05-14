from tkinter import Frame, LEFT, X
from pyeventbus3.pyeventbus3 import *

from src.Presentation.StyledTkinter import StyledTkinter
from .SymbolSelector import SymbolSelector


class RichTextInputMenu(Frame):
    def __init__(self, master):
        super().__init__(master, bg="grey75")

        self.master = master
        self.buttons = []
        self.init_buttons()
        self.symbol_selector = SymbolSelector(self)

        self.symbol_selector_open = False

    def init_buttons(self):
        self.add_button("Symbols", lambda: self.click_symbols())
        self.add_button("Functions", lambda: self.click_symbols())
        self.add_button("Set Image", lambda: self.click_symbols())

    def add_button(self, text, command):
        self.buttons.append(StyledTkinter.get_dark_button(self, text=text, command=command))

    def display(self):
        super().pack(expand=False, fill=X)

        for button in self.buttons:
            button.pack(side=LEFT, padx=(0, 5), pady=(0, 5))

    def click_symbols(self):
        if self.symbol_selector_open:
            self.symbol_selector.hide()
            self.symbol_selector_open = False
        else:
            self.symbol_selector_open = True
            self.symbol_selector.tkraise()
            self.symbol_selector.display()
