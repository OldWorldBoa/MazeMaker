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
        self.content = None

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

    def data(self, content):
        self.content = content

        return self

    def build(self):
        graph = self.create_graph()
        self.add_data(graph)

        return graph

    def create_graph(self):
        self.graph = BiDirectionalGraph()

        for row in range(max(self.rows, self.previewRows)):
            for col in range(max(self.columns, self.previewColumns)):
                vertex_type = self.get_vertex_type(row, col)

                if vertex_type != GraphDataType.SKIP:
                    vertex_id = str(row) + "," + str(col)
                    self.graph.add_vertex(vertex_id)
                    self.graph.set_vertex_data(vertex_id, GraphData(vertex_type, col, row))

                    self.add_edges(vertex_id, vertex_type, row, col)

        return self.graph

    def add_edges(self, vertex_id, vertex_type, row, col):
        if row > 0:
            self.graph.add_edge(vertex_id, str(row - 1) + "," + str(col))
            self.graph.set_edge_data(vertex_id, str(row - 1) + "," + str(col), GraphData(vertex_type, 0, 0))

        if col > 0:
            self.graph.add_edge(vertex_id, str(row) + "," + str(col - 1))
            self.graph.set_edge_data(vertex_id, str(row) + "," + str(col - 1), GraphData(vertex_type, 0, 0))

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

    def add_data(self, graph):
        if self.content is not None:
            solution_data = [x for x in self.content if x['part_of_answer'] == 1]
            filler_data = [x for x in self.content if x['part_of_answer'] == 0]

            num_data = len(solution_data)

            path = graph.get_random_path(
                "0,0",
                num_data + 1  # +1 for Finish square
            )

            if path:
                for i in range(0, num_data):
                    vertex = path[i]
                    next_vertex = path[i + 1]
                    content = self.solution_data[i]

                    graph.get_edge_data(vertex, next_vertex).content = content['answer']
                    graph.get_edge_data(vertex, next_vertex).part_of_answer = True
                    self.fill_vertex(graph, vertex, content)

                graph.get_vertex_data(path[num_data]).content = {"text": "Finish", "placed_images": []}

                other_vertices = [x for x in graph.vertices if x not in path]
                if other_vertices:
                    for i in range(0, len(other_vertices)):
                        self.fill_vertex(graph, other_vertices[i], filler_data[i])

    def fill_vertex(self, graph, vertex, content):
        graph.get_vertex_data(vertex).content = content['question']
        graph.get_vertex_data(vertex).part_of_answer = content['part_of_answer']

        neighbours = graph.vertices[vertex]
        if not neighbours:
            return

        answers = content['fillers']
        answers.append(content['answer'])

        for next_vertex in neighbours:
            edge_data = graph.get_edge_data(vertex, next_vertex)

            # This is set on the initial pass through with the actual solution, don't change those
            if not edge_data.content:
                edge_data.content = answers[neighbours.index(next_vertex)]
                edge_data.part_of_answer = False
