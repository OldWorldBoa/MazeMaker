import math

from threading import Lock
from tkinter import Frame, Canvas, BOTH, SUNKEN, Text, font, DISABLED, FLAT, X
from pyeventbus3.pyeventbus3 import *

from src.Presentation.StyledTkinter import StyledTkinter
from .GraphRendererMenu import GraphRendererMenu
from src.Business.Infrastructure.KillableThread import KillableThread
from src.Model.GraphDataType import GraphDataType
from src.Model.GraphRendererState import GraphRendererState
from src.Business.Builders.GraphBuilder import GraphBuilder
from src.Business.Events.UpdateGraph import UpdateGraph
from src.Business.Events.UpdateGraphPreview import UpdateGraphPreview
from src.Business.Events.GraphRendererStateLoaded import GraphRendererStateLoaded
from src.Business.Events.ResetGraphPreview import ResetGraphPreview
from src.Business.Events.GraphChanged import GraphChanged
from src.Business.Events.LoadGraphData import LoadGraphData
from src.Business.Events.ChangeQuestionHeight import ChangeQuestionHeight
from src.Business.Events.ChangeQuestionWidth import ChangeQuestionWidth
from src.Business.Events.ChangeAnswerLength import ChangeAnswerLength
from src.Business.Events.ChangeAnswerWidth import ChangeAnswerWidth
from src.Business.Decorators.ClampNegativeArgs import clamp_negative_args


class GraphRenderer(Frame):
    def __init__(self, master):
        super().__init__(master, borderwidth=1, relief=SUNKEN)
        PyBus.Instance().register(self, self.__class__.__name__)

        self.question_height = 100
        self.question_width = 100
        self.answer_length = 50
        self.answer_width = 50
        self.rows = 0
        self.columns = 0
        self.preview_rows = 0
        self.preview_columns = 0

        self.synchronizer = Lock()
        self.current_work = None
        self.canvas = Canvas(self, bg=StyledTkinter.get_light_color())
        self.menu = GraphRendererMenu(self, self.question_height,
                                      self.question_width,
                                      self.answer_length,
                                      self.answer_width)
        self.graph = None
        self.content = None
        self.drawn_edges = []

    def display(self, **kwargs):
        super().grid(kwargs)
        self.menu.display()
        self.canvas.pack(fill=BOTH, expand=True)

    @clamp_negative_args
    def update_graph_component_size(self, height, width):
        if self.question_height != height or self.question_width != width:
            self.question_height = height
            self.question_width = width
            self.draw()

    @clamp_negative_args
    def update_size(self, rows, columns):
        if self.rows != rows or self.columns != columns:
            self.rows = rows
            self.columns = columns
            self.refresh_graph()
            self.graph_changed()

    @clamp_negative_args
    def update_preview_size(self, preview_rows, preview_columns):
        if self.preview_rows != preview_rows or self.preview_columns != preview_columns:
            self.preview_rows = preview_rows
            self.preview_columns = preview_columns
            self.refresh_graph(redraw_data=False)

    def reset_preview(self):
        if self.preview_rows != self.rows or self.preview_columns != self.columns:
            self.preview_rows = self.rows
            self.preview_columns = self.columns
            self.refresh_graph()

    def refresh_graph(self, redraw_data=True):
        self.graph = GraphBuilder() \
            .current(self.rows, self.columns) \
            .preview(self.preview_rows, self.preview_columns) \
            .data(self.content if redraw_data else None) \
            .build()

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.drawn_edges.clear()

        for vertex in self.graph.vertices.keys():
            vertex_data = self.graph.get_vertex_data(vertex)

            if vertex_data.type != GraphDataType.SKIP:
                self.draw_vertex_with_edges(vertex)

    def draw_vertex_with_edges(self, vertex):
        data = self.graph.get_vertex_data(vertex)
        x = self.answer_length + data.x * self.question_width + data.x * self.answer_length
        y = self.answer_length + data.y * self.question_height + data.y * self.answer_length
        border_color = self.get_color_for_graph_data_type(data.type)
        fill_color = self.get_fill_color_for_graph_data_type(data.type)

        self.canvas.create_rectangle(x, y, x + self.question_width, y + self.question_height, outline=border_color,
                                     fill=fill_color)
        self.canvas.create_window((x + 1, y + 1), anchor="nw",
                                  window=self.make_content_widget(data.content, self.question_height,
                                                                  self.question_width))

        self.draw_edges(vertex)

    def draw_edges(self, vertex):
        for neighbour in self.graph.neighbours(vertex):
            edge_key = self.graph.get_edge_key(vertex, neighbour)
            if edge_key not in self.drawn_edges:
                self.draw_edge(vertex, neighbour)
                self.drawn_edges.append(edge_key)

    def draw_edge(self, vertex, next_vertex):
        x = self.get_edge_x(vertex, next_vertex)
        y = self.get_edge_y(vertex, next_vertex)
        x_size = self.get_x_size(vertex, next_vertex)
        y_size = self.get_y_size(vertex, next_vertex)
        edge_data = self.graph.get_edge_data(vertex, next_vertex)
        border_color = self.get_color_for_graph_data_type(edge_data.type)
        fill_color = self.get_fill_color_for_graph_data_type(edge_data.type)

        self.canvas.create_rectangle(x, y, x + x_size, y + y_size, outline=border_color, fill=fill_color)
        self.canvas.create_window((x + x_size / 2 + 1, y + 1), anchor="n",
                                  window=self.make_content_widget(edge_data.content, y_size, x_size))

    def get_x_size(self, vertex, next_vertex):
        vertex_data = self.graph.get_vertex_data(vertex)
        next_vertex_data = self.graph.get_vertex_data(next_vertex)

        if next_vertex_data.x - vertex_data.x == 0:
            return self.answer_width
        else:
            return self.answer_length

    def get_y_size(self, vertex, next_vertex):
        vertex_data = self.graph.get_vertex_data(vertex)
        next_vertex_data = self.graph.get_vertex_data(next_vertex)

        if next_vertex_data.y - vertex_data.y == 0:
            return self.answer_width
        else:
            return self.answer_length

    def make_content_widget(self, content, height, width):
        if content:
            frame = Frame(self, height=height - 2, width=width - 2)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)
            frame.pack()
            frame.pack_propagate(False)

            self.make_text_widget(content, frame)

            return frame

    @staticmethod
    def make_text_widget(content, frame):
        text = Text(frame, font=font.Font(size=16), relief=FLAT, width=1, height=1)
        text.insert("1.0", content["text"])

        images = content["placed_images"]
        if images:
            for image in images:
                text.image_create(image["index"], image=image["image"])

        text.tag_configure("center", justify='center')
        text.tag_add("center", "1.0", "end")
        text.pack(fill=BOTH, expand=True)
        text.config(state=DISABLED)

        return text

    def get_edge_x(self, vertex, next_vertex):
        vertex_data = self.graph.get_vertex_data(vertex)
        next_vertex_data = self.graph.get_vertex_data(next_vertex)
        center_x = vertex_data.x * self.question_width + \
                   (vertex_data.x + 1) * self.answer_length + self.question_width / 2

        return center_x + self.get_direction_modifier(next_vertex_data.x - vertex_data.x, self.question_width)

    def get_edge_y(self, vertex, next_vertex):
        vertex_data = self.graph.get_vertex_data(vertex)
        next_vertex_data = self.graph.get_vertex_data(next_vertex)
        center_y = vertex_data.y * self.question_height + \
                   (vertex_data.y + 1) * self.answer_length + self.question_height / 2

        return center_y + self.get_direction_modifier(next_vertex_data.y - vertex_data.y, self.question_height)

    # direction > 0: get distance to edge of box
    # direction == 0: get half of the width to move over
    # direction < 0: get the distance to the other edge of the box
    def get_direction_modifier(self, direction, scale):
        if direction > 0:
            return scale / 2
        elif direction == 0:
            return -self.answer_width / 2
        else:
            return -scale / 2 - self.answer_length

    def get_state_to_save(self):
        return GraphRendererState(self.graph, self.rows, self.columns)

    def load_state(self, state):
        self.graph = state.graph
        self.rows = state.rows
        self.preview_rows = state.rows
        self.columns = state.columns
        self.preview_columns = state.columns

    @staticmethod
    def get_color_for_graph_data_type(curr_type):
        if curr_type == GraphDataType.EXISTS:
            return "black"
        elif curr_type == GraphDataType.REMOVE:
            return "red"
        elif curr_type == GraphDataType.ADD:
            return "green"
        else:
            return ""

    @staticmethod
    def get_fill_color_for_graph_data_type(curr_type):
        if curr_type == GraphDataType.EXISTS:
            return "white"
        elif curr_type == GraphDataType.REMOVE:
            return "RosyBrown1"
        elif curr_type == GraphDataType.ADD:
            return "DarkSeaGreen1"
        else:
            return ""

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=UpdateGraph)
    def update_graph(self, event):
        rows = self.get_rows_from(event.y)
        cols = self.get_columns_from(event.x)

        if rows != self.rows or cols != self.columns:
            self.synchronizer.acquire()

            self.kill_current_work()
            self.current_work = KillableThread(
                target=self.update_size,
                args=(rows, cols,))
            self.current_work.start()

            self.synchronizer.release()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=UpdateGraphPreview)
    def update_graph_preview(self, event):
        rows = self.get_rows_from(event.y)
        cols = self.get_columns_from(event.x)

        if rows != self.preview_rows or cols != self.preview_columns:
            self.synchronizer.acquire()

            self.kill_current_work()
            self.current_work = KillableThread(
                target=self.update_preview_size,
                args=(rows, cols,))
            self.current_work.start()

            self.synchronizer.release()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=GraphRendererStateLoaded)
    def load_graph(self, event):
        self.synchronizer.acquire()

        self.kill_current_work()
        self.load_state(event.graph_renderer_state)
        self.current_work = KillableThread(target=self.draw)
        self.current_work.start()

        self.synchronizer.release()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=ResetGraphPreview)
    def reset_when_tool_changes(self, event):
        self.synchronizer.acquire()

        self.kill_current_work()
        self.current_work = KillableThread(target=self.reset_preview)
        self.current_work.start()

        self.synchronizer.release()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=LoadGraphData)
    def load_graph_data(self, event):
        self.synchronizer.acquire()

        self.kill_current_work()
        self.content = event.content
        self.current_work = KillableThread(target=self.refresh_graph)
        self.current_work.start()

        self.synchronizer.release()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=ChangeQuestionWidth)
    def change_question_width(self, event):
        self.question_width = int(event.new_width)
        self.draw()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=ChangeQuestionHeight)
    def change_question_width(self, event):
        self.question_height = int(event.new_height)
        self.draw()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=ChangeAnswerWidth)
    def change_answer_width(self, event):
        self.answer_width = int(event.new_width)
        self.draw()

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=ChangeAnswerLength)
    def change_answer_length(self, event):
        self.answer_length = int(event.new_length)
        self.draw()

    def graph_changed(self):
        PyBus.Instance().post(GraphChanged(self.rows, self.columns))

    def get_rows_from(self, y):
        return math.ceil((y - self.answer_length) / (self.question_width + self.answer_length))

    def get_columns_from(self, x):
        return math.ceil((x - self.answer_length) / (self.question_height + self.answer_length))

    def kill_current_work(self):
        if self.current_work is not None:
            self.current_work.kill()
            self.current_work.join()
