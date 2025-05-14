from ..Menu import Menu
from ..NumericEntry import NumericEntry
from ...Business.Tools.DrawMazeTool import DrawMazeTool
from ...Business.Events.SelectToolEvent import SelectToolEvent
from ...Business.Events.ChangeGraphWidth import ChangeGraphWidth
from ...Business.Events.ChangeGraphHeight import ChangeGraphHeight

from pyeventbus3.pyeventbus3 import *
from tkinter import Label, StringVar, LEFT


# The click button command handlers require one parameter,
# but it isn't currently used so we are ignoring the following:
# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyMethodParameters
class GraphRendererMenu(Menu):
    def __init__(self, master, initial_height, initial_width):
        super().__init__(master)

        self.master = master
        self.initial_height = initial_height
        self.initial_width = initial_width
        self.add_button("Draw Maze", self.click_draw_maze)

        self.height_label = Label(self, text="Height: ")
        self.height_container = StringVar()
        self.height_entry = NumericEntry(self, self.initial_height, textvariable=self.height_container)
        self.height_container.trace_add("write", self.change_height)

        self.width_label = Label(self, text="Width: ")
        self.width_container = StringVar()
        self.width_entry = NumericEntry(self, self.initial_width, textvariable=self.width_container)
        self.width_container.trace_add("write", self.change_width)

    def display(self):
        super().display()

        self.height_label.pack(side=LEFT, padx=(0, 5), pady=(0, 5))
        self.height_entry.pack(side=LEFT, padx=(0, 5), pady=(0, 5))
        self.width_label.pack(side=LEFT, padx=(0, 5), pady=(0, 5))
        self.width_entry.pack(side=LEFT, padx=(0, 5), pady=(0, 5))

    def click_draw_maze(click_event):
        PyBus.Instance().post(SelectToolEvent(DrawMazeTool()))

    def change_height(self, var, mode, name):
        PyBus.Instance().post(ChangeGraphHeight(self.height_container.get()))

    def change_width(self, var, mode, name):
        PyBus.Instance().post(ChangeGraphWidth(self.width_container.get()))
