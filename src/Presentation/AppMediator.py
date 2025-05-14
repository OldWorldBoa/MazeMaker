import pickle

from PIL import EpsImagePlugin, ImageGrab
from tkinter import Frame, BOTH

from pyeventbus3.pyeventbus3 import *

from .Footer import Footer
from .MainFrame import MainFrame
from .MainMenu import MainMenu
from .StyledTkinter import StyledTkinter
from .PrintDialogue import PrintDialogue
from src.Business.Events.SaveToFile import SaveToFile
from src.Business.Events.ExportAsImage import ExportAsImage
from src.Business.Events.PrintCanvas import PrintCanvas
from src.Business.Infrastructure.KeyPressHandler import KeyPressHandler
from src.Business.Infrastructure.MouseHandler import MouseHandler
from src.Model.ProgramState import ProgramState
from ..Model.Constants import Constants


class AppMediator(Frame):
    def __init__(self, master):
        super().__init__(master, borderwidth=5, height=650, width=960, bg=StyledTkinter.get_dark_color())

        PyBus.Instance().register(self, self.__class__.__name__)

        self.master = master
        self.master.title("Maze Maker")

        self.menu = MainMenu(self)
        self.content_frame = MainFrame(self)
        self.footer = Footer(self)

        self.tickNum = 0
        self.key_press_handler = KeyPressHandler(master)
        self.mouse_handler = MouseHandler(self.content_frame.graph_renderer.canvas)

        self.set_ghost_script_binary()

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
        if not str(event.file).endswith('.png'):
            event.file += '.png'

        self.content_frame.graph_renderer.canvas.configure(bg="white")
        self.export_to_file(event.file)
        self.content_frame.graph_renderer.canvas.configure(bg=StyledTkinter.get_light_color())

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=PrintCanvas)
    def print_canvas(self, event):
        self.content_frame.graph_renderer.canvas.configure(bg="white")
        show_solution = self.content_frame.graph_renderer.show_solution
        if show_solution:
            self.content_frame.graph_renderer.show_solution = False
            self.content_frame.graph_renderer.draw()

        self.export_to_file(Constants.temp_png_file)

        self.content_frame.graph_renderer.show_solution = True
        self.content_frame.graph_renderer.draw()

        self.export_to_file(Constants.temp_png_soln_file)

        if not show_solution:
            self.content_frame.graph_renderer.show_solution = False
            self.content_frame.graph_renderer.draw()

        self.content_frame.graph_renderer.canvas.configure(bg=StyledTkinter.get_light_color())
        print_dialogue = PrintDialogue()
        print_dialogue.display()

    def export_to_file(self, file_name):
        # Let the screen have time to stop changing
        time.sleep(0.05)

        x = self.content_frame.graph_renderer.winfo_rootx() + self.content_frame.graph_renderer.canvas.winfo_x()
        y = self.content_frame.graph_renderer.winfo_rooty() + self.content_frame.graph_renderer.canvas.winfo_y()
        xx = x + self.content_frame.graph_renderer.get_used_width()
        yy = y + self.content_frame.graph_renderer.get_used_height()
        ImageGrab.grab(bbox=(x, y, xx, yy)).save(file_name)

    @staticmethod
    def set_ghost_script_binary():
        root_dir = os.path.dirname(os.path.abspath(__file__))
        binary_path = os.path.join(root_dir, "..\\..\\lib\\gs9.54.0\\bin\\gswin64c")
        EpsImagePlugin.gs_windows_binary = binary_path
