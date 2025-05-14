from ...Model.BiDirectionalGraph import BiDirectionalGraph
from ...Model.GraphDataType import GraphDataType
from ...Model.GraphData import GraphData
from ..Decorators.ClampNegativeArgs import ClampNegativeArgs

class GraphBuilder():
  def __init__(self):
    self.graph = BiDirectionalGraph()
    self.rows = 0
    self.columns = 0
    self.previewRows = 0
    self.previewColumns = 0

  @ClampNegativeArgs
  def current(self, rows, columns):
    self.rows = rows
    self.columns = columns

    return self

  @ClampNegativeArgs
  def preview(self, previewRows, previewColumns):
    self.previewRows = previewRows
    self.previewColumns = previewColumns

    return self

  def build(self):
    return self.createGraph()

  def createGraph(self):
    self.graph = BiDirectionalGraph()

    for i in range(max(self.rows, self.previewRows)):
      for j in range(max(self.columns, self.previewColumns)):
        vertexType = self.getVertexType(i, j)

        if vertexType != GraphDataType.SKIP:
          vertexId = str(i) + "," + str(j)
          self.graph.addVertex(vertexId)
          self.graph.setVertexData(vertexId, GraphData(vertexType, i, j))

          if i > 0:
            self.graph.addEdge(vertexId, str(i-1) + "," + str(j))
            self.graph.setEdgeData(vertexId, str(i-1) + "," + str(j), GraphData(vertexType, 0, 0))

          if j > 0:
            self.graph.addEdge(vertexId, str(i) + "," + str(j-1))
            self.graph.setEdgeData(vertexId, str(i) + "," + str(j-1), GraphData(vertexType, 0, 0))
            
    return self.graph

  def getVertexType(self, row, column):
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