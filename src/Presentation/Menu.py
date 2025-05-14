from tkinter import Frame, LEFT, X
from pyeventbus3.pyeventbus3 import *

from ..Business.Events.SelectToolEvent import SelectToolEvent
from .StyledTkinter import StyledTkinter
from ..Business.Tools.DrawMazeTool import DrawMazeTool
from ..Business.Tools.SaveTool import SaveTool
from ..Business.Tools.LoadTool import LoadTool
from ..Business.Tools.ExportTool import ExportTool
from ..Business.Tools.EditContentTool import EditContentTool
from ..Business.Tools.PrintTool import PrintTool


# The click button command handlers require one parameter,
# but it isn't currently used so we are ignoring the following:
# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyMethodParameters
class Menu(Frame):
    def __init__(self, master):
        super().__init__(master, bg="grey")

        self.master = master
        self.buttons = []
        self.init_buttons()

    def init_buttons(self):
        self.add_button("Save", self.click_save)
        self.add_button("Load", self.click_load)
        self.add_button("Export", self.click_export)
        self.add_button("Draw Maze", self.click_draw_maze)
        self.add_button("Edit Content", self.click_edit_content)
        self.add_button("Print", self.click_print)

    def add_button(self, text, command):
        self.buttons.append(StyledTkinter.get_styled_button(self, text=text, command=command))

    def display(self):
        super().pack(expand=False, fill=X)

        for button in self.buttons:
            button.pack(side=LEFT, padx=(0, 5), pady=(0, 5))

    def click_save(click_event):
        PyBus.Instance().post(SelectToolEvent(SaveTool()))

    def click_load(click_event):
        PyBus.Instance().post(SelectToolEvent(LoadTool()))

    def click_export(click_event):
        PyBus.Instance().post(SelectToolEvent(ExportTool()))

    def click_draw_maze(click_event):
        PyBus.Instance().post(SelectToolEvent(DrawMazeTool()))

    def click_edit_content(click_event):
        PyBus.Instance().post(SelectToolEvent(EditContentTool()))

    def click_print(click_event):
        PyBus.Instance().post(SelectToolEvent(PrintTool()))
