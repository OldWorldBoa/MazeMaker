from PIL import Image, ImageTk
from tkinter import Frame, Text, BOTH, INSERT, font, END, TclError

from ..StyledTkinter import StyledTkinter
from .RichTextInputMenu import RichTextInputMenu


class RichTextInput(Frame):
    def __init__(self, master):
        super().__init__(master, bg=StyledTkinter.get_medium_color())

        self.menu = RichTextInputMenu(self, self.input_symbol, self.set_input_image)
        self.input = Text(self, height=8, font=font.Font(size=16))
        self.images = {}
        self.image_cache = []

    def display(self, **kwargs):
        super().grid(kwargs)

        self.menu.display()
        self.input.pack(fill=BOTH)

    def input_symbol(self, symbol):
        self.input.insert(INSERT, symbol)

    def set_input_image(self, filename):
        size = 128, 128
        pil_image = Image.open(filename)
        pil_image.thumbnail(size)
        key = self.get_image_key(filename)

        self.images[key] = pil_image

        shown_image = ImageTk.PhotoImage(pil_image)
        self.image_cache.append(shown_image)
        self.input.image_create(INSERT, image=shown_image, name=key)

    def get_image_key(self, filename):
        key = filename
        count = 0

        while key in self.images:
            count += 1
            key = filename + str(count)

        return key

    def get_content(self):
        text = self.input.get("1.0", 'end-1c')
        placed_images = []

        for key in self.images.keys():
            try:
                index = self.input.index(key)
                indexed_image = {"index": index, "key": key, "image": self.images[key]}
                placed_images.append(indexed_image)
            except TclError:
                pass

        return {"text": text, "placed_images": placed_images}

    def load_content(self, load_data):
        self.input.insert("1.0", load_data["text"])

        images = load_data["placed_images"]
        if images:
            for image in images:
                self.images[image["key"]] = image["image"]
                shown_image = ImageTk.PhotoImage(image["image"])
                self.image_cache.append(shown_image)
                self.input.image_create(image["index"], image=shown_image)

    def insert(self, index, content):
        self.input.insert(index, content)
