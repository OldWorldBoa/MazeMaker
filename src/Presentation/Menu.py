from tkinter import Button, Frame, LEFT, X, FLAT
from pyeventbus3.pyeventbus3 import *

from ..Business.Events.SelectToolEvent import SelectToolEvent 
from ..Business.Tools.Tool import Tool
from ..Business.Tools.DrawMazeTool import DrawMazeTool
from ..Business.Tools.SaveTool import SaveTool
from ..Business.Tools.LoadTool import LoadTool
from ..Business.Tools.ExportTool import ExportTool

class Menu(Frame):
  def __init__(self, master):
    super().__init__(master, bg="grey")

    self.master = master
    self.initButtons()

  def initButtons(self):
    self.buttons = []

    self.addButton("Save", self.ClickSave)
    self.addButton("Load", self.ClickLoad)
    self.addButton("Export", self.ClickExport)
    self.addButton("Draw Maze", self.ClickDrawMaze)
    self.addButton("Edit Text", self.ClickEditText)

  def addButton(self, text, command):
    self.buttons.append(
      Button(self, text=text, command=command, relief=FLAT,
        bg="gray40", fg="gray88", activebackground="gray15",
        activeforeground="gray63"))

  def pack(self):
    super().pack(expand=False, fill=X)

    for button in self.buttons:
      button.pack(side=LEFT, padx=(0, 5), pady=(0, 5))

  def ClickSave(clickEvent):
    PyBus.Instance().post(SelectToolEvent(SaveTool()))

  def ClickLoad(clickEvent):
    PyBus.Instance().post(SelectToolEvent(LoadTool()))

  def ClickExport(clickEvent):
    PyBus.Instance().post(SelectToolEvent(ExportTool()))

  def ClickDrawMaze(clickEvent):
    PyBus.Instance().post(SelectToolEvent(DrawMazeTool()))

  def ClickEditText(clickEvent):
    PyBus.Instance().post(SelectToolEvent(Tool()))