from .StyledTkinter import StyledTkinter
from .TabContainer import TabContainer
from ..Business.Events.CloseOtherInputs import CloseOtherInputs
from src.Presentation.RichTextInput.RichTextInput import RichTextInput

from tkinter import Frame, Label, StringVar, NSEW, LEFT, Checkbutton, IntVar, END, INSERT
from pyeventbus3.pyeventbus3 import *


class ContentInput(Frame):
    def __init__(self, master, question_number, load_data=None):
        super().__init__(master, bg=StyledTkinter.get_medium_color())

        self.isInSolution = IntVar(value=1)
        self.display_open = False
        self.question_number = question_number

        self.header_border = Frame(self, bg=StyledTkinter.get_dark_color())
        self.header = Frame(self.header_border, bg=StyledTkinter.get_medium_color())
        self.toggle_text = StringVar(value="+")
        self.toggle_display = StyledTkinter.get_dark_button(self.header,
                                                            textvariable=self.toggle_text,
                                                            command=self.toggle_input_display,
                                                            width=2)
        self.header_title = Label(self.header,
                                  bg=StyledTkinter.get_medium_color(),
                                  text="Question " + str(question_number + 1))
        self.header_is_in_solution_indicator = Label(self.header,
                                                     text="In Solution",
                                                     bg=StyledTkinter.get_medium_color())

        self.question_title_row = Frame(self, bg=StyledTkinter.get_medium_color())
        self.question_in_solution = Checkbutton(self.question_title_row,
                                                text='Use in solution',
                                                variable=self.isInSolution,
                                                bg=StyledTkinter.get_medium_color(),
                                                command=self.update_is_in_solution_indicator)
        self.question_label = Label(self.question_title_row, bg=StyledTkinter.get_medium_color(), text="Question")
        self.question = RichTextInput(self)

        self.answer_tabs = TabContainer(self)
        self.answer = RichTextInput(self.answer_tabs.create_empty_tab("Answer"))

        self.fillers = []
        for i in range(3):
            self.fillers.append(RichTextInput(self.answer_tabs.create_empty_tab("Filler " + str(i + 1))))

        self.load(load_data)

    def update_is_in_solution_indicator(self):
        if self.isInSolution.get():
            self.header_is_in_solution_indicator.config(text="In Solution")
        else:
            self.header_is_in_solution_indicator.config(text="")

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
        self.header.columnconfigure(2, weight=1)

        self.header.grid(row=0, column=0, pady=(0, 2), columnspan=2, sticky=NSEW)
        self.header_border.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        self.toggle_display.grid(row=0, column=0, sticky="nw")
        self.header_title.grid(row=0, column=1, sticky=NSEW)
        self.header_is_in_solution_indicator.grid(row=0, column=2, sticky="nw")

    def fill_with_test_data(self, index):
        ContentInput.update_input(self.question.input, "Question" + str(index + 1))
        ContentInput.update_input(self.answer.input, "Answer" + str(index + 1))

        for filler in self.fillers:
            filler_index = self.fillers.index(filler)
            ContentInput.update_input(filler.input, "Q" + str(index + 1) + " Filler" + str(filler_index + 1))

    @staticmethod
    def update_input(input_to_update, text):
        curr_text = input_to_update.get("1.0", END)

        if curr_text.strip() == "":
            input_to_update.insert(INSERT, text)

    def toggle_input_display(self):
        if self.display_open:
            self.close_input_display()
        elif not self.display_open:
            self.open_input_display()

    def open_input_display(self):
        self.question_title_row.grid(row=1, column=0, sticky="nw", pady=(6, 0))
        self.question_label.pack(side=LEFT, padx=(0, 5), pady=(0, 5))
        self.question_in_solution.pack(side=LEFT, padx=(0, 5), pady=(0, 5))
        self.question.display(row=2, column=0, sticky="new")
        self.answer_tabs.display(row=1, rowspan=2, column=1, pady=(5, 0), sticky=NSEW)
        self.answer.display()
        for filler in self.fillers:
            filler.display()
        self.toggle_text.set("-")
        self.display_open = True

        PyBus.Instance().post(CloseOtherInputs(self.question_number))

    def close_input_display(self):
        self.question_title_row.grid_remove()
        self.question.grid_remove()
        self.answer_tabs.grid_remove()
        self.toggle_text.set("+")
        self.display_open = False

    def load(self, load_data):
        if load_data is not None:
            self.question.insert(0, load_data['question'])
            self.answer.insert(0, load_data['answer'])

    def is_filled(self):
        answer_content = self.answer.get_content()
        if not answer_content["text"] and not answer_content["placed_images"]:
            return False

        question_content = self.question.get_content()
        if not question_content["text"] and not question_content["placed_images"]:
            return False

        for filler in self.fillers:
            filler_content = filler.get_content()

            if not filler_content["text"] and not filler_content["placed_images"]:
                return False

        return True

    def get_as_dict(self):
        return {
            'part_of_answer': self.isInSolution.get(),
            'question': self.question.get_content(),
            'answer': self.answer.get_content(),
            'fillers': [x.get_content() for x in self.fillers]
        }
