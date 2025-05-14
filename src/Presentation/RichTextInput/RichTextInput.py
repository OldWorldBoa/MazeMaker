from PIL import Image, ImageTk
from tkinter import Frame, Text, BOTH, INSERT, font, END

from ..StyledTkinter import StyledTkinter
from .RichTextInputMenu import RichTextInputMenu


class RichTextInput(Frame):
    def __init__(self, master):
        super().__init__(master, bg=StyledTkinter.get_medium_color())

        self.menu = RichTextInputMenu(self, self.input_symbol, self.set_input_image)
        self.input = Text(self, height=8, font=font.Font(size=16))
        self.images = []

    def display(self, **kwargs):
        super().grid(kwargs)

        self.menu.display()
        self.input.pack(fill=BOTH)

    def input_symbol(self, symbol):
        self.input.insert(INSERT, symbol)

    def set_input_image(self, filename):
        size = 128, 128
        pil_image = Image.open(filename)
        tk_image = ImageTk.PhotoImage(pil_image)
        self.images.append(tk_image)

        self.input.image_create(INSERT, image=self.images[-1], name=filename)
        x = 2

    def get_text(self):
        return self.input.get("1.0", 'end-1c')

    def insert(self, index, content):
        self.input.insert(index, content)
