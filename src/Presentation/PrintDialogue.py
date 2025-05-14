import win32print
import win32ui
from PIL import Image, ImageWin

from tkinter import Toplevel, StringVar, Label, ttk

from .StyledTkinter import StyledTkinter


class PrintDialogue(Toplevel):
    def __init__(self):
        super().__init__()

        self.done_button = StyledTkinter.get_styled_button(self, text="Print", command=lambda: self.print())
        self.info = Label(self, text="select Printer")
        self.printers = ttk.Combobox(self, width=35, textvariable=StringVar())
        self.printers['values'] = self.get_printers()

    @staticmethod
    def get_printers():
        print_list = []

        printers = list(win32print.EnumPrinters(2))
        for i in printers:
            print_list.append(i[2])

        return print_list

    def display(self):
        self.info.pack(pady=10)
        self.printers.pack(padx=10)
        self.done_button.pack(pady=10)

        self.title("Print maze")

    def print(self):
        #
        # Constants for GetDeviceCaps
        #
        #
        # HORZRES / VERTRES = printable area
        #
        HORZRES = 8
        VERTRES = 10
        #
        # LOGPIXELS = dots per inch
        #
        LOGPIXELSX = 88
        LOGPIXELSY = 90
        #
        # PHYSICALWIDTH/HEIGHT = total area
        #
        PHYSICALWIDTH = 110
        PHYSICALHEIGHT = 111
        #
        # PHYSICALOFFSETX/Y = left / top margin
        #
        PHYSICALOFFSETX = 112
        PHYSICALOFFSETY = 113

        file_name = "C:\\temp\\mm_tmp.jpg"

        #
        # You can only write a Device-independent bitmap
        #  directly to a Windows device context; therefore
        #  we need (for ease) to use the Python Imaging
        #  Library to manipulate the image.
        #
        # Create a device context from a named printer
        #  and assess the printable size of the paper.
        #
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(self.printers.get())
        printable_area = hDC.GetDeviceCaps(HORZRES), hDC.GetDeviceCaps(VERTRES)
        printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
        printer_margins = hDC.GetDeviceCaps(PHYSICALOFFSETX), hDC.GetDeviceCaps(PHYSICALOFFSETY)

        #
        # Open the image, rotate it if it's wider than
        #  it is high, and work out how much to multiply
        #  each pixel by to get it as big as possible on
        #  the page without distorting.
        #
        bmp = Image.open(file_name)
        if bmp.size[0] > bmp.size[1]:
            bmp = bmp.rotate(90)

        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min(ratios)

        #
        # Start the print job, and draw the bitmap to
        #  the printer device at the scaled size.
        #
        hDC.StartDoc(file_name)
        hDC.StartPage()

        dib = ImageWin.Dib(bmp)
        scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
        x1 = int((printer_size[0] - scaled_width) / 2)
        y1 = int((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height
        dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()

        self.destroy()
