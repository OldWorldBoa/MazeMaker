import pickle
import io
import cv2

from PIL import Image, EpsImagePlugin, ImageChops
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
from ..Events.PrintCanvas import PrintCanvas
from ...Presentation.PrintDialogue import PrintDialogue


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
        if not str(event.file).endswith('.png'):
            event.file += '.png'

        self.export_to_file(event.file)

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=PrintCanvas)
    def print_canvas(self, event):
        self.export_to_file('C:\\temp\\mm_tmp.png')

        print_dialogue = PrintDialogue()
        print_dialogue.display()

    def export_to_file(self, file_name):
        ps = self.content_frame.graph_renderer.canvas.postscript()
        self.set_ghost_script_binary()
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save(file_name)
        self.trim(file_name)

    # https://www.semicolonworld.com/question/60108/how-to-remove-extra-whitespace-from-image-in-opencv
    @staticmethod
    def trim(file_name):
        # Load image, grayscale, Gaussian blur, Otsu's threshold
        image = cv2.imread(file_name)
        original = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (25, 25), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Perform morph operations, first open to remove noise, then close to combine
        noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, noise_kernel, iterations=2)
        close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=3)

        # Find enclosing bounding-box and crop ROI
        coordinates = cv2.findNonZero(close)
        x, y, w, h = cv2.boundingRect(coordinates)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        crop = original[y:y + h, x:x + w]

        cv2.imwrite(file_name, crop)

    @staticmethod
    def set_ghost_script_binary():
        root_dir = os.path.dirname(os.path.abspath(__file__))
        binary_path = os.path.join(root_dir, "..\\..\\..\\lib\\gs9.54.0\\bin\\gswin64c")
        EpsImagePlugin.gs_windows_binary = binary_path
