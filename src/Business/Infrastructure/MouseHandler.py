import time

from pyeventbus3.pyeventbus3 import *

from ..Tools.Tool import Tool
from ..Events.SelectToolEvent import SelectToolEvent
from ..Events.ResetGraphPreview import ResetGraphPreview


class MouseHandler(Tool):
    def __init__(self, master):
        super().__init__()
        PyBus.Instance().register(self, self.__class__.__name__)

        self.master = master
        self.tool = Tool()

        master.bind("<Button 1>", self.tool.mouse_click)
        master.bind("<Motion>", self.tool.mouse_move)
        master.bind('<MouseWheel>', self.on_mouse_wheel)

    @staticmethod
    def on_mouse_wheel(mouse_wheel_event):
        print(mouse_wheel_event)

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=SelectToolEvent)
    def set_active_tool(self, event):
        self.tool = event.tool
        self.master.bind("<Button 1>", self.tool.mouse_click)
        self.master.bind("<Motion>", self.tool.mouse_move)

        # Wait for a bit to make sure all UpdateGraphPreview commands have finished
        time.sleep(0.1)
        PyBus.Instance().post(ResetGraphPreview())

        self.tool.run("EXECUTE")
