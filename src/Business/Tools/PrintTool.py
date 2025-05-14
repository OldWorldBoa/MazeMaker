from pyeventbus3.pyeventbus3 import *

from .Tool import Tool
from ..Events.PrintCanvas import PrintCanvas


class PrintTool(Tool):
    def __init__(self):
        super().__init__()

    def run(self, command, **kwargs):
        if command == "EXECUTE":
            PyBus.Instance().post(PrintCanvas())
