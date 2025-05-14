from random import randrange

class BiDirectionalGraph():
  def __init__(self):
    self.vertices = {}
    self.vertexData = {}
    self.edgeData = {}

  def adjacent(self, vertex, nextVertex):
    if (vertex in self.vertices):
      if (nextVertex in self.vertices[vertex]):
        return True

    return False

  def neighbours(self, vertex):
    if (vertex in self.vertices):
      return self.vertices[vertex]

    return []

  def addVertex(self, vertex, adjVertices = []):
    self.vertices[vertex] = adjVertices.copy()

  def removeVertex(self, vertex):
    if (vertex in self.vertices):
      neighbours = self.neighbours(vertex)
      self.vertices.pop(vertex)

      for neighbour in neighbours:
        self.vertices[neighbour].remove(vertex)

  def addEdge(self, vertex, nextVertex):
    if (vertex in self.vertices and nextVertex in self.vertices):
      self.vertices[vertex].append(nextVertex)
      self.vertices[nextVertex].append(vertex)

  def removeEdge(self, vertex, nextVertex):
    if (vertex in self.vertices and nextVertex in self.vertices):
      self.vertices[vertex].remove(nextVertex)
      self.vertices[nextVertex].remove(vertex)

  def getVertexData(self, vertex):
    if (vertex in self.vertexData):
      return self.vertexData[vertex]

    return {}

  def setVertexData(self, vertex, data):
    if (vertex in self.vertices):
      self.vertexData[vertex] = data

  def getEdgeData(self, vertex, nextVertex):
    key = self.getEdgeKey(vertex, nextVertex)
    if (key in self.edgeData):
      return self.edgeData[key]

    return {}

  def setEdgeData(self, vertex, nextVertex, data):
    if (vertex in self.vertices and nextVertex in self.vertices and vertex != nextVertex):
      if (nextVertex in self.vertices[vertex] and vertex in self.vertices[nextVertex]):
        key = self.getEdgeKey(vertex, nextVertex)
        self.edgeData[key] = data

  def getEdgeKey(self, vertex, nextVertex):
    return min(vertex, nextVertex) + max(vertex, nextVertex)

  def getRandomPath(self, start, end, coveragePercent):
    if (start in self.vertices and end in self.vertices and 
        coveragePercent >= 2 / len(self.vertices) * 100 and coveragePercent <= 100):
      path = []
      done = False

      paths = self.findAllPaths(start, end)
      pathsWithcoverage = []

      for path in paths:
        if (len(path) / len(self.vertices) * 100 >= coveragePercent):
          pathsWithcoverage.append(path)

      numPaths = len(pathsWithcoverage)
      if numPaths == 1:
        return pathsWithcoverage[0]
      elif numPaths > 1:
        return pathsWithcoverage[randrange(numPaths)]

    return []

  def findAllPaths(self, start, end, path=[]):
    if start not in self.vertices or end not in self.vertices:
      return []

    path.append(start)

    if start == end:
      return [path]

    paths = []

    for vertex in self.vertices[start]:
      if vertex not in path:
        newpaths = self.findAllPaths(vertex, end, path.copy())
        for newpath in newpaths:
          paths.append(newpath)
          
    return paths