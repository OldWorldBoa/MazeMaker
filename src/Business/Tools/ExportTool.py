
from tkinter import filedialog
from pyeventbus3.pyeventbus3 import *

from .Tool import Tool
from ..Events.ExportAsImage import ExportAsImage


class ExportTool(Tool):
    def __init__(self):
        super().__init__()

    def run(self, command, **kwargs):
        if command == "EXECUTE":
            files = [('PNG', '*.png')]
            file = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)

            PyBus.Instance().post(ExportAsImage(file))
