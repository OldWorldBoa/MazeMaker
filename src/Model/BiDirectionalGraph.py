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

    def get_random_path(self, start, length):
        if start in self.vertices:
            done = False

            visited_paths = BiDirectionalGraph()
            visited_paths.add_vertex(start)
            curr_path = [start]
            curr_vertex = start

            while not done:
                available_neighbours = self.get_available_neighbours(curr_vertex, curr_path, visited_paths)

                if len(available_neighbours) == 0:
                    done = self.remove_last_element(curr_path)
                    curr_vertex = curr_path[0]
                else:
                    next_vertex = available_neighbours[randrange(len(available_neighbours))]
                    visited_paths.add_vertex(next_vertex)
                    visited_paths.add_edge(curr_vertex, next_vertex)
                    curr_path.append(next_vertex)
                    curr_vertex = next_vertex

                    if len(curr_path) >= length:
                        done = True

            return curr_path
        else:
            return []

    def get_available_neighbours(self, curr_vertex, curr_path, visited_paths):
        visited_neighbours = visited_paths.vertices[curr_vertex]
        vertex_neighbours = self.vertices[curr_vertex]

        return [x for x in vertex_neighbours if x not in visited_neighbours and x not in curr_path]

    @staticmethod
    def remove_last_element(self, curr_path):
        curr_path.pop()

        if not curr_path:
            return True

        return False

