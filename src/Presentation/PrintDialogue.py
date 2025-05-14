import win32print
import win32api
import img2pdf
import os


from tkinter import Toplevel, StringVar, Label, ttk, Canvas, filedialog

from .StyledTkinter import StyledTkinter


class PrintDialogue(Toplevel):
    def __init__(self):
        super().__init__()

        self.temp_png_file = "C:\\temp\\mm_tmp.png"
        self.temp_pdf_file = "C:\\temp\\mm_tmp.pdf"
        self.pdf_printer_name = "Print to PDF"
        self.done_button = StyledTkinter.get_styled_button(self, text="Print", command=lambda: self.complete_print())
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

    def print_to_pdf(self, f_name=''):
        if f_name != '':
            print_file = f_name
        else:
            files = [('PDF', '*.pdf')]
            file = filedialog.asksaveasfilename(filetypes=files, defaultextension=files)
            print_file = file

        if print_file == '' or print_file is None:
            return

        with open(print_file, "wb") as f:
            f.write(img2pdf.convert(self.temp_png_file))

    def print(self):
        printer_name = self.printers.get()

        if printer_name == self.pdf_printer_name:
            self.print_to_pdf()
        else:
            self.print_to_pdf(self.temp_pdf_file)
            win32print.SetDefaultPrinter(printer_name)
            os.startfile(self.temp_pdf_file, "print")
