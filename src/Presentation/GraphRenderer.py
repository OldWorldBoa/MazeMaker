import math

from tkinter import Frame, Canvas, BOTH, SUNKEN
from pyeventbus3.pyeventbus3 import *

from ..Model.BiDirectionalGraph import BiDirectionalGraph
from ..Model.GraphDataType import GraphDataType
from ..Model.GraphData import GraphData
from ..Business.Builders.GraphBuilder import GraphBuilder
from ..Business.Events.UpdateGraph import UpdateGraph
from ..Business.Events.UpdateGraphPreview import UpdateGraphPreview
from ..Business.Events.GraphLoaded import GraphLoaded
from ..Business.Decorators.ClampNegativeArgs import ClampNegativeArgs

class GraphRenderer(Frame):
  def __init__(self, master):
    super().__init__(master, borderwidth=1, relief=SUNKEN)
    PyBus.Instance().register(self, self.__class__.__name__)

    self.canvas = Canvas(self, bg="gray82")
    self.graph = None
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

  @ClampNegativeArgs
  def updateGraphComponentSize(self, height, width):
    if (self.height != height or self.width != width):
      self.height = height
      self.width = width
      self.draw()

  @ClampNegativeArgs
  def updateSize(self, rows, columns):
    if (self.rows != rows or self.columns != columns):
      self.rows = rows
      self.columns = columns
      self.refreshGraph()

  @ClampNegativeArgs
  def updatePreviewSize(self, previewRows, previewColumns):
    if (self.previewRows != previewRows or self.previewColumns != previewColumns):
      self.previewRows = previewRows
      self.previewColumns = previewColumns
      self.refreshGraph()

  def resetPreview(self):
    if (self.previewRows != self.rows or self.previewColumns != self.columns):
      self.previewRows = self.rows
      self.previewColumns = self.columns
      self.refreshGraph()
      
  def refreshGraph(self):
    self.graph = GraphBuilder() \
      .current(self.rows, self.columns) \
      .preview(self.previewRows, self.previewColumns) \
      .build()

    self.draw()

  def draw(self):
    self.canvas.delete("all")
    currRow = 0
    currCol = 0
    
    for vertex in self.graph.vertices.keys():
      vertexData = self.graph.getVertexData(vertex)

      if (vertexData.type != GraphDataType.SKIP):
        self.drawRect(vertexData)
      
      currRow += 1
      if (currRow == max(self.rows, self.previewRows)):
        currRow = 0
        currCol += 1

  def drawRect(self, data):
    x = self.padding + data.x * self.width + data.x * self.padding
    y = self.padding + data.y * self.height + data.y * self.padding
    color = self.getColorForGraphDataType(data.type)

    self.canvas.create_rectangle(x, y, x + self.width, y + self.height, outline=color, fill="white")

    self.canvas.create_text(
      x+self.width/2,
      y+self.height/2,
      fill="black",
      font="Times 20 italic bold",
      text=data.text)

  def getColorForGraphDataType(self, currType):
    if currType == GraphDataType.EXISTS:
      return "black"
    elif currType == GraphDataType.REMOVE:
      return "red"
    elif currType == GraphDataType.ADD:
      return "green"
    else:
      return ""

  @subscribe(threadMode = Mode.BACKGROUND, onEvent=UpdateGraph)
  def updateGraph(self, event):
      self.updateSize(self.getRowsFrom(event.x), self.getColumnsFrom(event.y))

  @subscribe(threadMode = Mode.BACKGROUND, onEvent=UpdateGraphPreview)
  def updateGraphPreview(self, event):
      self.updatePreviewSize(self.getRowsFrom(event.x), self.getColumnsFrom(event.y))

  @subscribe(threadMode = Mode.BACKGROUND, onEvent=GraphLoaded)
  def loadGraph(self, event):
    self.graph = event.graph
    self.draw()

  def getRowsFrom(self, y):
    return math.ceil((y - self.padding) / (self.width + self.padding));

  def getColumnsFrom(self, x):
    return math.ceil((x - self.padding) / (self.height + self.padding));
