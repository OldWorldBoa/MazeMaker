from threading import Lock
from tkinter import Frame
from pyeventbus3.pyeventbus3 import *

from ..Business.Events.GraphChanged import GraphChanged
from ..Business.Events.LoadGraphData import LoadGraphData
from ..Business.Events.ContentLoaded import ContentLoaded
from ..Business.Builders.GraphBuilder import GraphBuilder
from .ContentInput import ContentInput
from .StyledTkinter import StyledTkinter


class ContentEditor(Frame):
    def __init__(self, master):
        super().__init__(master, bg="gray75", pady=10, padx=10)

        PyBus.Instance().register(self, self.__class__.__name__)

        self.master = master
        self.generate_button = StyledTkinter.get_styled_button(self, text="Generate Maze", command=self.generate_maze)
        self.inputs = []
        self.synchronizer = Lock()

    def grid(self, **kwargs):
        super().grid(kwargs, sticky="nesw")

        self.columnconfigure(0, weight=1)
        self.generate_button.grid(row=0, pady=(0, 10))

    def get_savable_inputs(self):
        return [x.get_as_dict() for x in self.inputs]

    def load_saved_inputs(self, inputs):
        for curr_input in self.inputs:
            curr_input.grid_forget()
        self.inputs = []

        for i in range(0, len(inputs)):
            loaded_input = ContentInput(self, inputs[i])
            loaded_input.grid(row=i + 1, pady=(0, 5))
            self.inputs.append(loaded_input)

    def generate_maze(self):
        content = [x.get_as_dict() for x in self.inputs if x.is_filled()]
        PyBus.Instance().post(LoadGraphData(content))

    def update_size(self, rows, columns):
        max_path_length = ContentEditor.get_max_path_length(rows, columns) - 1  # -1 for Finish square
        new_vertices = rows * columns
        curr_length = len(self.inputs)

        if 0 <= curr_length < max_path_length:
            # add items to the end
            for i in range(0, max_path_length - curr_length):
                new_input = ContentInput(self)
                new_input.grid(row=curr_length + i + 1, pady=(0, 5))
                self.inputs.append(new_input)
        elif max_path_length < curr_length:
            # hide items over the end
            entries_to_hide = self.inputs[max_path_length:len(self.inputs)]
            self.inputs = self.inputs[:max_path_length]

            for i in range(0, len(entries_to_hide)):
                entries_to_hide[i].grid_forget()

    @staticmethod
    def get_max_path_length(rows, columns):
        if rows > 0 and columns > 0:
            graph = GraphBuilder() \
                .current(rows, columns) \
                .preview(rows, columns) \
                .build()

            paths = graph.find_all_paths('0,0', str(rows - 1) + ',' + str(columns - 1))
            path_lengths = [len(i) for i in paths]

            return max(path_lengths)
        else:
            return 0

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=GraphChanged)
    def update_content_editor(self, event):
        self.synchronizer.acquire()
        self.update_size(event.rows, event.columns)
        self.synchronizer.release()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=ContentLoaded)
    def load_content(self, event):
        self.synchronizer.acquire()
        self.load_saved_inputs(event.content)
        self.synchronizer.release()
