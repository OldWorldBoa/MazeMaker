from tkinter import Frame, BOTH
from pyeventbus3.pyeventbus3 import *

from ...Presentation.Footer import Footer
from ...Presentation.GraphRenderer import GraphRenderer
from ...Presentation.Menu import Menu
from ..Events.SelectToolEvent import SelectToolEvent
from ..Tools.Tool import Tool
from .KeyPressHandler import KeyPressHandler


class AppMediator(Frame):
    def __init__(self, master):
        super().__init__(master, borderwidth=5, height=650, width=960, bg="grey")

        PyBus.Instance().register(self, self.__class__.__name__)

        self.master = master
        self.master.title("Maze Maker")

        self.menu = Menu(self)
        self.graphRenderer = GraphRenderer(self)
        self.footer = Footer(self)

        self.tickNum = 0
        self.tool = Tool()
        self.keyPressHandler = KeyPressHandler(master)

    def pack(self):
        super().pack(expand=True, fill=BOTH)

        self.menu.pack()
        self.graphRenderer.pack()
        self.graphRenderer.updateSize(4, 4)
        self.graphRenderer.updatePreviewSize(4, 4)
        self.footer.pack()

    def tick(self):
        self.footer.fpsIndicator.update_fps(self.tickNum)
        self.tickNum += 1
        self.master.after(10, self.tick)

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=SelectToolEvent)
    def select_tool(self, event):
        self.tool = event.tool
        self.tool.run("EXECUTE", graph=self.graphRenderer.graph, canvas=self.graphRenderer.canvas)
        self.graphRenderer.resetPreview()
        self.graphRenderer.canvas.bind("<Button 1>", self.tool.mouse_click)
        self.graphRenderer.canvas.bind("<Motion>", self.tool.mouse_move)
