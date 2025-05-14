from ..Menu import Menu
from ...Business.Tools.DrawMazeTool import DrawMazeTool
from ...Business.Events.SelectToolEvent import SelectToolEvent

from pyeventbus3.pyeventbus3 import *


# The click button command handlers require one parameter,
# but it isn't currently used so we are ignoring the following:
# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyMethodParameters
class GraphRendererMenu(Menu):
    def __init__(self, master):
        super().__init__(master)

        self.add_button("Draw Maze", self.click_draw_maze)
        self.add_button("Change Height", self.change_height)
        self.add_button("Change Width", self.change_width)

    def click_draw_maze(click_event):
        PyBus.Instance().post(SelectToolEvent(DrawMazeTool()))

    def change_height(click_event):
        pass

    def change_width(click_event):
        pass
