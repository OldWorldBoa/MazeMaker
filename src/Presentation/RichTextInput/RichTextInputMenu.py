from tkinter.filedialog import askopenfilename

from src.Presentation.Menu import Menu
from .SymbolSelector import SymbolSelector


class RichTextInputMenu(Menu):
    def __init__(self, master, input_symbol_callback, set_image_callback):
        super().__init__(master, bg="grey75")

        self.input_symbol_callback = input_symbol_callback
        self.set_image_callback = set_image_callback

        self.symbol_selector = None

        self.add_button("Symbols", self.click_symbols)
        self.add_button("Functions", self.click_symbols)
        self.add_button("Set Image", self.click_set_image)

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
