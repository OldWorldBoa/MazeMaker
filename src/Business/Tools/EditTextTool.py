from pyeventbus3.pyeventbus3 import *

from .Tool import Tool
from ..Events.EditTextAt import EditTextAt


class EditTextTool(Tool):
    def __init__(self):
        super().__init__()

    def mouse_click(self, event):
        PyBus.Instance().post(EditTextAt(event.x, event.y))
