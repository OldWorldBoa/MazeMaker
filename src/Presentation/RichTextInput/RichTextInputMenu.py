from tkinter import Frame, LEFT, X
from tkinter.filedialog import askopenfilename
from pyeventbus3.pyeventbus3 import *

from src.Presentation.StyledTkinter import StyledTkinter
from .SymbolSelector import SymbolSelector


class RichTextInputMenu(Frame):
    def __init__(self, master, input_symbol_callback, set_image_callback):
        super().__init__(master, bg="grey75")

        self.input_symbol_callback = input_symbol_callback
        self.set_image_callback = set_image_callback

        self.master = master
        self.buttons = []
        self.symbol_selector = None
        self.init_buttons()

    def init_buttons(self):
        self.add_button("Symbols", lambda: self.click_symbols())
        self.add_button("Functions", lambda: self.click_symbols())
        self.add_button("Set Image", lambda: self.click_set_image())

    def add_button(self, text, command):
        self.buttons.append(StyledTkinter.get_dark_button(self, text=text, command=command))

    def display(self):
        super().pack(expand=False, fill=X)

        for button in self.buttons:
            button.pack(side=LEFT, padx=(0, 5), pady=(0, 5))

    def click_symbols(self):
        if self.symbol_selector is not None:
            self.symbol_selector.destroy()

        x = self.winfo_pointerx()
        y = self.winfo_pointery()
        self.symbol_selector = SymbolSelector(self, x, y, self.input_symbol_callback)
        self.symbol_selector.focus_set()

    def click_set_image(self):
        filename = askopenfilename(title="Select your image",
                                   filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg")])
        self.set_image_callback(filename)
