from threading import Lock
from tkinter import Frame, LEFT, X, Label, StringVar

from .StyledTkinter import StyledTkinter
from .NumericEntry import NumericEntry


class Menu(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, kwargs)

        self.master = master
        self.lock = Lock()
        self.elements = []

    def add_button(self, text, command):
        self.elements.append(StyledTkinter.get_dark_button(self, text=text, command=command))

    def add_debounced_button(self, text, command):
        self.elements.append(StyledTkinter.get_dark_button(self, text=text,
                                                           command=lambda: self.debounced_command(command)))

    def add_entry(self, label_text, entry):
        label = Label(self, text=label_text)

        self.elements.append(label)
        self.elements.append(entry)

    def debounced_command(self, command):
        if self.lock.acquire(blocking=False):
            try:
                command()
            finally:
                self.lock.release()

    def display(self, **kwargs):
        super().pack(kwargs, expand=False, fill=X)

        for element in self.elements:
            element.pack(side=LEFT, padx=(0, 5))
