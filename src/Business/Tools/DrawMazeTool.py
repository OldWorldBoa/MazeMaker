from pyeventbus3.pyeventbus3 import *

from .Tool import Tool
from ..Events.UpdateGraphPreview import UpdateGraphPreview
from ..Events.UpdateGraph import UpdateGraph
from ..Events.SelectToolEvent import SelectToolEvent


class DrawMazeTool(Tool):
    def __init__(self):
        super().__init__()
        pass

    def mouse_click(self, event):
        PyBus.Instance().post(UpdateGraph(event.x, event.y))
        PyBus.Instance().post(SelectToolEvent(Tool()))

    def mouse_move(self, event):
        PyBus.Instance().post(UpdateGraphPreview(event.x, event.y))
