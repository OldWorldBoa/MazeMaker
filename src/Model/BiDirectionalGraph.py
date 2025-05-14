from random import randrange


class BiDirectionalGraph:
    def __init__(self):
        self.vertices = {}
        self.vertexData = {}
        self.edgeData = {}

    def adjacent(self, vertex, next_vertex):
        if vertex in self.vertices:
            if next_vertex in self.vertices[vertex]:
                return True

        return False

    def neighbours(self, vertex):
        if vertex in self.vertices:
            return self.vertices[vertex]

        return []

    def add_vertex(self, vertex, adj_vertices=None):
        if adj_vertices is None:
            adj_vertices = []

        self.vertices[vertex] = adj_vertices.copy()

    def remove_vertex(self, vertex):
        if vertex in self.vertices:
            neighbours = self.neighbours(vertex)
            self.vertices.pop(vertex)

            for neighbour in neighbours:
                self.vertices[neighbour].remove(vertex)

    def add_edge(self, vertex, next_vertex):
        if vertex in self.vertices and next_vertex in self.vertices:
            self.vertices[vertex].append(next_vertex)
            self.vertices[next_vertex].append(vertex)

    def remove_edge(self, vertex, next_vertex):
        if vertex in self.vertices and next_vertex in self.vertices:
            self.vertices[vertex].remove(next_vertex)
            self.vertices[next_vertex].remove(vertex)

    def get_vertex_data(self, vertex):
        if vertex in self.vertexData:
            return self.vertexData[vertex]

        return {}

    def set_vertex_data(self, vertex, data):
        if vertex in self.vertices:
            self.vertexData[vertex] = data

    def get_edge_data(self, vertex, next_vertex):
        key = self.get_edge_key(vertex, next_vertex)
        if key in self.edgeData:
            return self.edgeData[key]

        return {}

    def set_edge_data(self, vertex, next_vertex, data):
        if vertex in self.vertices and next_vertex in self.vertices and vertex != next_vertex:
            if next_vertex in self.vertices[vertex] and vertex in self.vertices[next_vertex]:
                key = self.get_edge_key(vertex, next_vertex)
                self.edgeData[key] = data

    @staticmethod
    def get_edge_key(vertex, next_vertex):
        return min(vertex, next_vertex) + max(vertex, next_vertex)

    def get_random_path(self, start, end, length):
        if (start in self.vertices and end in self.vertices):
            paths = self.find_all_paths(start, end)
            paths_with_length = []

            for path in paths:
                if len(path) == length:
                    paths_with_length.append(path)

            num_paths = len(paths_with_length)
            if num_paths == 1:
                return paths_with_length[0]
            elif num_paths > 1:
                return paths_with_length[randrange(num_paths)]

        return []

    def find_all_paths(self, start, end, path=None):
        if path is None:
            path = []

        if start not in self.vertices or end not in self.vertices:
            return []

        path.append(start)

        if start == end:
            return [path]

        paths = []

        for vertex in self.vertices[start]:
            if vertex not in path:
                new_paths = self.find_all_paths(vertex, end, path.copy())
                for new_path in new_paths:
                    paths.append(new_path)

        return paths
