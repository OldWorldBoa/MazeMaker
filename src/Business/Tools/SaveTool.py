import pickle

from tkinter import filedialog

from .Tool import Tool


class SaveTool(Tool):
    def __init__(self):
        super().__init__()

    def run(self, command, **kwargs):
        if command == "EXECUTE":
            file = filedialog.asksaveasfilename(defaultextension=".mmpy")

            if file != '':
                graph = kwargs["graph"]
                pickle.dump(graph, open(file, 'wb'))
