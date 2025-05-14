import pickle

from tkinter import filedialog
from pyeventbus3.pyeventbus3 import *

from .Tool import Tool
from ..Events.GraphLoaded import GraphLoaded


class LoadTool(Tool):
    def __init__(self):
        super().__init__()

    def run(self, command, **kwargs):
        if command == "EXECUTE":
            file = filedialog.askopenfilename(defaultextension=".mmpy")

            if file != '':
                graph = pickle.load(open(file, 'rb'))
                PyBus.Instance().post(GraphLoaded(graph))
