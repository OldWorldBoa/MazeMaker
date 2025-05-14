from ...Model.BiDirectionalGraph import BiDirectionalGraph
from ...Model.GraphDataType import GraphDataType
from ...Model.GraphData import GraphData
from ..Decorators.ClampNegativeArgs import clamp_negative_args


class GraphBuilder:
    def __init__(self):
        self.graph = BiDirectionalGraph()
        self.rows = 0
        self.columns = 0
        self.previewRows = 0
        self.previewColumns = 0

    @clamp_negative_args
    def current(self, rows, columns):
        self.rows = rows
        self.columns = columns

        return self

    @clamp_negative_args
    def preview(self, preview_rows, preview_columns):
        self.previewRows = preview_rows
        self.previewColumns = preview_columns

        return self

    def build(self):
        return self.create_graph()

    def create_graph(self):
        self.graph = BiDirectionalGraph()

        for i in range(max(self.rows, self.previewRows)):
            for j in range(max(self.columns, self.previewColumns)):
                vertex_type = self.get_vertex_type(i, j)

                if vertex_type != GraphDataType.SKIP:
                    vertex_id = str(i) + "," + str(j)
                    self.graph.add_vertex(vertex_id)
                    self.graph.set_vertex_data(vertex_id, GraphData(vertex_type, i, j))

                    if i > 0:
                        self.graph.add_edge(vertex_id, str(i - 1) + "," + str(j))
                        self.graph.set_edge_data(vertex_id, str(i - 1) + "," + str(j), GraphData(vertex_type, 0, 0))

                    if j > 0:
                        self.graph.add_edge(vertex_id, str(i) + "," + str(j - 1))
                        self.graph.set_edge_data(vertex_id, str(i) + "," + str(j - 1), GraphData(vertex_type, 0, 0))

        return self.graph

    def get_vertex_type(self, row, column):
        if (row < self.rows and row < self.previewRows and
                column < self.columns and column < self.previewColumns):
            return GraphDataType.EXISTS
        elif ((row >= self.rows and column < self.previewColumns) or
              (column >= self.columns and row < self.previewRows)):
            return GraphDataType.ADD
        elif ((row < self.rows and column >= self.previewColumns) or
              (column < self.columns and row >= self.previewRows)):
            return GraphDataType.REMOVE
        else:
            return GraphDataType.SKIP
