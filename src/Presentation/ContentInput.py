from tkinter import Frame, Label, StringVar
from pyeventbus3.pyeventbus3 import *

from .StyledTkinter import StyledTkinter
from ..Business.Events.CloseOtherInputs import CloseOtherInputs
from src.Presentation.RichTextInput.RichTextInput import RichTextInput


class ContentInput(Frame):
    def __init__(self, master, question_number, load_data=None):
        super().__init__(master, bg=StyledTkinter.get_medium_color())

        self.display_open = False
        self.question_number = question_number

        self.header_border = Frame(self, bg=StyledTkinter.get_dark_color())
        self.header = Frame(self.header_border, bg=StyledTkinter.get_medium_color())
        self.toggle_text = StringVar(value="+")
        self.toggle_display = StyledTkinter.get_dark_button(self.header,
                                                            textvariable=self.toggle_text,
                                                            command=self.toggle_input_display,
                                                            width=2)
        self.toggle_display_label = Label(self.header,
                                          bg=StyledTkinter.get_medium_color(),
                                          text="Question " + str(question_number + 1))

        self.question_label = Label(self, bg=StyledTkinter.get_medium_color(), text="Question")
        self.question = RichTextInput(self)
        self.answer_label = Label(self, bg=StyledTkinter.get_medium_color(), text="Answer")
        self.answer = RichTextInput(self)

        self.load(load_data)

    def display(self, **kwargs):
        super().grid(kwargs, column=0, sticky="new")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.header_border.rowconfigure(0, weight=1)
        self.header_border.columnconfigure(0, weight=1)
        self.header.rowconfigure(0, weight=1)
        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=9)

        self.header.grid(row=0, column=0, pady=(0, 2), columnspan=2, sticky="news")
        self.header_border.grid(row=0, column=0, columnspan=2, sticky="news")
        self.toggle_display.grid(row=0, column=0, sticky="nw")
        self.toggle_display_label.grid(row=0, column=1, sticky="news")

    def toggle_input_display(self):
        if self.display_open:
            self.close_input_display()
        elif not self.display_open:
            self.open_input_display()

    def open_input_display(self):
        self.question_label.grid(row=1, column=0, sticky="nw")
        self.question.display(row=2, column=0, sticky="new")
        self.answer_label.grid(row=1, column=1, sticky="nw")
        self.answer.display(row=2, column=1, sticky="new")
        self.toggle_text.set("-")
        self.display_open = True

        PyBus.Instance().post(CloseOtherInputs(self.question_number))

    def close_input_display(self):
        self.question_label.grid_remove()
        self.question.grid_remove()
        self.answer_label.grid_remove()
        self.answer.grid_remove()
        self.toggle_text.set("+")
        self.display_open = False

    def load(self, load_data):
        if load_data is not None:
            self.question.insert(0, load_data['question'])
            self.answer.insert(0, load_data['answer'])

    def is_filled(self):
        question_content = self.question.get_content()
        answer_content = self.answer.get_content()

        if (question_content["text"] != "" or question_content["placed_images"] != []) and \
                (answer_content["text"] != "" or answer_content["placed_images"] != []):
            return True
        return False

    def get_as_dict(self):
        return {'question': self.question.get_content(), 'answer': self.answer.get_content()}
