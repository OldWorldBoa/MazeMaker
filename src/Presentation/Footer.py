from tkinter import Frame, X, Label, LEFT
from pyeventbus3.pyeventbus3 import *

from .FpsIndicator import FpsIndicator
from .StyledTkinter import StyledTkinter
from ..Business.Events.DisplayMessage import DisplayMessage
from ..Model.MessageSeverity import MessageSeverity


class Footer(Frame):
    def __init__(self, master):
        super().__init__(master, bg=StyledTkinter.get_dark_color())

        PyBus.Instance().register(self, self.__class__.__name__)

        self.master = master
        self.message = Label(self,
                             fg=StyledTkinter.get_light_color(),
                             bg=StyledTkinter.get_dark_color(),
                             text="Welcome!")
        self.fpsIndicator = FpsIndicator(self)

    def display(self):
        super().pack(expand=False, fill=X, pady=(5, 0))

        self.fpsIndicator.display()
        self.message.pack(side=LEFT, padx=(0, 5), pady=(0, 5))

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=DisplayMessage)
    def display_message(self, event):
        if event.message_severity == MessageSeverity.WARNING:
            self.message.config(fg="RosyBrown1")

        self.message.config(text=event.text)
