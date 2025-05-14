from tkinter import Frame, BOTH, W
from pyeventbus3.pyeventbus3 import *

from .ContentEditor import ContentEditor
from .GraphRenderer import GraphRenderer
from..Business.Events.ToggleContentEditor import ToggleContentEditor


class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master, bg="grey")

        PyBus.Instance().register(self, self.__class__.__name__)

        self.content_editor_shown = False
        self.graph_renderer = GraphRenderer(self)
        self.content_editor = ContentEditor(self)

    def display(self):
        super().pack(expand=True, fill=BOTH)

        self.hide_content_editor()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.graph_renderer.display(row=0, column=0, sticky="nesw")

    def toggle_content_editor(self):
        if not self.content_editor_shown:
            self.show_content_editor()
        else:
            self.hide_content_editor()

    def show_content_editor(self):
        self.columnconfigure(1, weight=1)
        self.content_editor.display(row=0, column=1, sticky="nesw", padx=(15, 0))
        self.content_editor_shown = True

    def hide_content_editor(self):
        self.columnconfigure(1, weight=0)
        self.content_editor.grid_forget()
        self.content_editor_shown = False

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=ToggleContentEditor)
    def handle_toggle_content_editor(self, event):
        self.toggle_content_editor()
