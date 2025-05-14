import pickle
import io

from PIL import Image
from tkinter import Frame, BOTH
from pyeventbus3.pyeventbus3 import *

from ...Presentation.Footer import Footer
from ...Presentation.MainFrame import MainFrame
from ...Presentation.Menu import Menu
from ..Events.SaveToFile import SaveToFile
from ..Events.ExportAsImage import ExportAsImage
from .KeyPressHandler import KeyPressHandler
from .MouseHandler import MouseHandler
from ...Model.ProgramState import ProgramState


class AppMediator(Frame):
    def __init__(self, master):
        super().__init__(master, borderwidth=5, height=650, width=960, bg="grey")

        PyBus.Instance().register(self, self.__class__.__name__)

        self.master = master
        self.master.title("Maze Maker")

        self.menu = Menu(self)
        self.content_frame = MainFrame(self)
        self.footer = Footer(self)

        self.tickNum = 0
        self.key_press_handler = KeyPressHandler(master)
        self.mouse_handler = MouseHandler(self.content_frame.graph_renderer.canvas)

    def display(self):
        super().pack(expand=True, fill=BOTH)

        self.menu.display()
        self.content_frame.display()
        self.footer.display()

    def tick(self):
        self.footer.fpsIndicator.update_fps(self.tickNum)
        self.tickNum += 1
        self.master.after(10, self.tick)

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=SaveToFile)
    def save_to_file(self, event):
        save_object = ProgramState(self.content_frame.graph_renderer.get_state_to_save(),
                                   self.content_frame.content_editor.get_savable_inputs())
        pickle.dump(save_object, open(event.file, 'wb'))

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=ExportAsImage)
    def export_as_image(self, event):
        canvas = self.content_frame.graph_renderer.canvas
        ps = canvas.postscript(colormode='color')
        im = Image.open(io.BytesIO(ps.encode('utf-8')))
        im.save(event.file + '.jpg')
