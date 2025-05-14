import pickle

from tkinter import filedialog
from pyeventbus3.pyeventbus3 import *

from .Tool import Tool
from ..Events.GraphRendererStateLoaded import GraphRendererStateLoaded
from ..Events.ContentLoaded import ContentLoaded


class LoadTool(Tool):
    def __init__(self):
        super().__init__()

    def run(self, command, **kwargs):
        if command == "EXECUTE":
            files = [('Maze Maker Saves', '*.mmpy')]
            file = filedialog.askopenfilename(filetypes=files, defaultextension=files)

            if file != '':
                program_state = pickle.load(open(file, 'rb'))
                PyBus.Instance().post(GraphRendererStateLoaded(program_state.graph_renderer_state))
                PyBus.Instance().post(ContentLoaded(program_state.content))
