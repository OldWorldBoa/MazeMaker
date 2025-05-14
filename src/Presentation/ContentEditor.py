from threading import Lock
from tkinter import Frame, Canvas, Scrollbar, RIGHT, LEFT, TOP, X, Y, BOTH, VERTICAL
from pyeventbus3.pyeventbus3 import *

from ..Business.Events.GraphChanged import GraphChanged
from ..Business.Events.LoadGraphData import LoadGraphData
from ..Business.Events.ContentLoaded import ContentLoaded
from ..Business.Events.CloseOtherInputs import CloseOtherInputs
from ..Business.Events.DisplayMessage import DisplayMessage
from .ContentInput import ContentInput
from .StyledTkinter import StyledTkinter
from ..Model.MessageSeverity import MessageSeverity


class ContentEditor(Frame):
    def __init__(self, master):
        super().__init__(master, bg="gray75", pady=10, padx=10)

        PyBus.Instance().register(self, self.__class__.__name__)

        self.master = master
        self.inner_content_frame = Frame(self, bg="gray75")
        self.scrollable_canvas = Canvas(self.inner_content_frame, bd=0, highlightthickness=0, relief='ridge',
                                        bg="gray75")
        self.content_frame = Frame(self.inner_content_frame, bg="gray75")
        self.canvas_frame = self.scrollable_canvas.create_window((0, 0), anchor="nw", window=self.content_frame)
        self.content_scrollbar = Scrollbar(self.inner_content_frame, orient=VERTICAL,
                                           command=self.scrollable_canvas.yview, bg="gray75")
        self.scrollable_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.scrollable_canvas.config(yscrollcommand=self.content_scrollbar.set)
        self.generate_button = StyledTkinter.get_dark_button(self, text="Generate Maze", command=self.generate_maze)
        self.inputs = []
        self.synchronizer = Lock()

    def display(self, **kwargs):
        super().grid(kwargs, sticky="nesw")

        self.generate_button.pack(side=TOP, fill=X, pady=(0, 2))
        self.inner_content_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.scrollable_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        self.content_scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollable_canvas.bind('<Configure>', self.change_width)
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.content_frame.columnconfigure(0, weight=1)

    def on_mousewheel(self, event):
        self.scrollable_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def change_width(self, event):
        self.scrollable_canvas.itemconfig(self.canvas_frame, width=event.width)

    def on_frame_configure(self, event):
        # Reset the scroll region to encompass the inner frame
        bbox = self.scrollable_canvas.bbox("all")
        x, y, width, height = bbox
        if height < self.scrollable_canvas.winfo_height():
            bbox = x, y, width, self.scrollable_canvas.winfo_height()

        self.scrollable_canvas.configure(scrollregion=bbox)

    def get_savable_inputs(self):
        return [x.get_as_dict() for x in self.inputs]

    def load_saved_inputs(self, inputs):
        for curr_input in self.inputs:
            curr_input.grid_forget()

        self.inputs = [ContentInput(self.content_frame, i, inputs[i]) for i in range(len(inputs))]

        for i in range(len(self.inputs)):
            self.inputs[i].display(row=i, pady=(0, 5))

    def generate_maze(self):
        if False not in [x.is_filled() for x in self.inputs]:
            content = [x.get_as_dict() for x in self.inputs]
            PyBus.Instance().post(LoadGraphData(content))
        else:
            PyBus.Instance().post(
                DisplayMessage("Please fill in all questions, answers and fillers", MessageSeverity.WARNING))

    def update_size(self, rows, columns):
        max_path_length = (rows * columns) - 1  # -1 for Finish square
        curr_length = len(self.inputs)

        if 0 <= curr_length < max_path_length:
            # add items to the end
            for i in range(0, max_path_length - curr_length):
                new_input = ContentInput(self.content_frame, curr_length + i)
                new_input.display(row=curr_length + i + 1, pady=(0, 5))
                self.inputs.append(new_input)
        elif max_path_length < curr_length:
            # hide items over the end
            entries_to_hide = self.inputs[max_path_length:len(self.inputs)]
            self.inputs = self.inputs[:max_path_length]

            for i in range(0, len(entries_to_hide)):
                entries_to_hide[i].grid_forget()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=CloseOtherInputs)
    def close_other_content_inputs(self, event):
        for i in range(len(self.inputs)):
            if i != event.except_index:
                self.inputs[i].close_input_display()

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
