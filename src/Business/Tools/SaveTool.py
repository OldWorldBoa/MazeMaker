from pyeventbus3.pyeventbus3 import *
from tkinter import filedialog

from .Tool import Tool
from ..Events.SaveToFile import SaveToFile


class SaveTool(Tool):
    def __init__(self):
        super().__init__()

    def run(self, command, **kwargs):
        if command == "EXECUTE":
            files = [('Maze Maker Saves', '*.mmpy')]
            file = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)

            if file != '':
                PyBus.Instance().post(SaveToFile(file))
