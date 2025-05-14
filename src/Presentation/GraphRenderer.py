import math

from tkinter import Frame, Canvas, BOTH, SUNKEN
from pyeventbus3.pyeventbus3 import *

from ..Model.GraphDataType import GraphDataType
from ..Business.Builders.GraphBuilder import GraphBuilder
from ..Business.Events.UpdateGraph import UpdateGraph
from ..Business.Events.UpdateGraphPreview import UpdateGraphPreview
from ..Business.Events.GraphLoaded import GraphLoaded
from ..Business.Decorators.ClampNegativeArgs import clamp_negative_args


class GraphRenderer(Frame):
    def __init__(self, master):
        super().__init__(master, borderwidth=1, relief=SUNKEN)
        PyBus.Instance().register(self, self.__class__.__name__)

        self.canvas = Canvas(self, bg="gray82")
        self.graph = None
        self.drawn_edges = []
        self.height = 100
        self.width = 100
        self.padding = 50
        self.rows = 0
        self.columns = 0
        self.previewRows = 0
        self.previewColumns = 0

    def pack(self):
        super().pack(fill=BOTH, expand=True)
        self.canvas.pack(fill=BOTH, expand=True)

    @clamp_negative_args
    def update_graph_component_size(self, height, width):
        if self.height != height or self.width != width:
            self.height = height
            self.width = width
            self.draw()

    @clamp_negative_args
    def update_size(self, rows, columns):
        if self.rows != rows or self.columns != columns:
            self.rows = rows
            self.columns = columns
            self.refresh_graph()

    @clamp_negative_args
    def update_preview_size(self, preview_rows, preview_columns):
        if self.previewRows != preview_rows or self.previewColumns != preview_columns:
            self.previewRows = preview_rows
            self.previewColumns = preview_columns

            try:
                self.refresh_graph()
            except AttributeError as ae:
                print("Error updating preview size to ", preview_rows, "rows and", preview_columns,
                      "columns. Error message:", ae)

    def reset_preview(self):
        if self.previewRows != self.rows or self.previewColumns != self.columns:
            self.previewRows = self.rows
            self.previewColumns = self.columns
            self.refresh_graph()

    def refresh_graph(self):
        self.graph = GraphBuilder() \
            .current(self.rows, self.columns) \
            .preview(self.previewRows, self.previewColumns) \
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
        x = self.padding + data.x * self.width + data.x * self.padding
        y = self.padding + data.y * self.height + data.y * self.padding
        color = self.get_color_for_graph_data_type(data.type)

        self.canvas.create_rectangle(x, y, x + self.width, y + self.height, outline=color, fill="white")
        self.canvas.create_text(x + self.width / 2, y + self.height / 2, fill="black", font="Times 20 italic bold",
                                text=data.text)

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
        edge_data = self.graph.get_edge_data(vertex, next_vertex)
        color = self.get_color_for_graph_data_type(edge_data.type)

        self.canvas.create_rectangle(x, y, x + self.padding, y + self.padding, outline=color, fill="white")
        self.canvas.create_text(x + self.padding / 2, y + self.padding / 2, fill="black", font="Times 20 italic bold",
                                text=edge_data.text)

    def get_edge_x(self, vertex, next_vertex):
        vertex_data = self.graph.get_vertex_data(vertex)
        next_vertex_data = self.graph.get_vertex_data(next_vertex)
        x = self.padding + vertex_data.x * self.width + vertex_data.x * self.padding + self.width / 2

        return x + self.get_direction_modifier(next_vertex_data.x - vertex_data.x)

    def get_edge_y(self, vertex, next_vertex):
        vertex_data = self.graph.get_vertex_data(vertex)
        next_vertex_data = self.graph.get_vertex_data(next_vertex)
        y = self.padding + vertex_data.y * self.height + vertex_data.y * self.padding + self.height / 2

        return y + self.get_direction_modifier(next_vertex_data.y - vertex_data.y)

    def get_direction_modifier(self, direction):
        if direction > 0:
            return self.width / 2
        elif direction == 0:
            return -self.padding / 2
        else:  # direction < 0
            return -self.width / 2 - self.padding

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

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=UpdateGraph)
    def update_graph(self, event):
        self.update_size(self.get_rows_from(event.y), self.get_columns_from(event.x))

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=UpdateGraphPreview)
    def update_graph_preview(self, event):
        self.update_preview_size(self.get_rows_from(event.y), self.get_columns_from(event.x))

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=GraphLoaded)
    def load_graph(self, event):
        self.graph = event.graph
        self.draw()

    def get_rows_from(self, y):
        return math.ceil((y - self.padding) / (self.width + self.padding))

    def get_columns_from(self, x):
        return math.ceil((x - self.padding) / (self.height + self.padding))
