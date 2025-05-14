import win32print
import img2pdf

from tkinter import Toplevel, StringVar, Label, ttk, Canvas, filedialog
from pyeventbus3.pyeventbus3 import *

from .StyledTkinter import StyledTkinter
from ..Model.Constants import Constants
from ..Business.Events.DisplayMessage import DisplayMessage
from ..Model.MessageSeverity import MessageSeverity


class PrintDialogue(Toplevel):
    def __init__(self):
        super().__init__()

        self.pdf_printer_name = "Print to PDF"
        self.done_button = StyledTkinter.get_dark_button(self, text="Print", command=lambda: self.complete_print())
        self.info = Label(self, text="Select Printer")
        self.preview = Canvas(self)
        self.printers = ttk.Combobox(self, width=35, textvariable=StringVar())
        self.printers['values'] = self.get_printers()

        self.virtual_margin = 100

    def get_printers(self):
        print_list = [self.pdf_printer_name]
        printers = list(win32print.EnumPrinters(2))

        for i in printers:
            if "pdf" not in i[2].lower():
                print_list.append(i[2])

        return print_list

    def display(self):
        self.info.pack(pady=10)
        self.printers.pack(padx=10)
        self.done_button.pack(pady=10)

        self.title("Print maze")

    def complete_print(self):
        self.print()
        self.destroy()

    @staticmethod
    def print_to_pdf(f_name=''):
        if f_name != '':
            print_file = f_name
        else:
            files = [('PDF', '*.pdf')]
            file = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
            print_file = file

        if print_file == '' or print_file is None:
            return

        try:
            with open(print_file, "wb") as f:
                f.write(img2pdf.convert(Constants.temp_png_file, Constants.temp_png_soln_file))

            return True
        except PermissionError as pe:
            PyBus.Instance().post(DisplayMessage(
                "Unable to save \"" + print_file + "\" due to lack of permissions. Check if it's open already.",
                MessageSeverity.ERROR
            ))

            return False

    def print(self):
        printer_name = self.printers.get()

        if printer_name == self.pdf_printer_name:
            PrintDialogue.print_to_pdf()
        else:
            if PrintDialogue.print_to_pdf(Constants.temp_pdf_file):
                win32print.SetDefaultPrinter(printer_name)
                os.startfile(Constants.temp_pdf_file, "print")
