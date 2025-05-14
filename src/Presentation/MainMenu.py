from pyeventbus3.pyeventbus3 import *

from ..Business.Events.SelectToolEvent import SelectToolEvent
from .StyledTkinter import StyledTkinter
from .Menu import Menu
from ..Business.Tools.DrawMazeTool import DrawMazeTool
from ..Business.Tools.SaveTool import SaveTool
from ..Business.Tools.LoadTool import LoadTool
from ..Business.Tools.ExportTool import ExportTool
from ..Business.Tools.EditContentTool import EditContentTool
from ..Business.Tools.PrintTool import PrintTool


# The click button command handlers require one parameter,
# but it isn't currently used so we are ignoring the following:
# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyMethodParameters
class MainMenu(Menu):
    def __init__(self, master):
        super().__init__(master, bg=StyledTkinter.get_dark_color())

        self.add_button("Save", self.click_save)
        self.add_button("Load", self.click_load)
        self.add_button("Export", self.click_export)
        self.add_button("Edit Content", self.click_edit_content)
        self.add_button("Print", self.click_print)

    def click_save(click_event):
        PyBus.Instance().post(SelectToolEvent(SaveTool()))

    def click_load(click_event):
        PyBus.Instance().post(SelectToolEvent(LoadTool()))

    def click_export(click_event):
        PyBus.Instance().post(SelectToolEvent(ExportTool()))

    def click_edit_content(click_event):
        PyBus.Instance().post(SelectToolEvent(EditContentTool()))

    def click_print(click_event):
        PyBus.Instance().post(SelectToolEvent(PrintTool()))
