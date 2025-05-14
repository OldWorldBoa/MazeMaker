from .StyledTkinter import StyledTkinter
from .TabContainer import TabContainer
from ..Business.Events.CloseOtherInputs import CloseOtherInputs
from src.Presentation.RichTextInput.RichTextInput import RichTextInput

from tkinter import Frame, Label, StringVar, X, LEFT, Checkbutton, IntVar, END, INSERT, BOTH
from pyeventbus3.pyeventbus3 import *


class ContentInput(Frame):
    def __init__(self, master, question_number, load_data=None):
        super().__init__(master, bg=StyledTkinter.get_medium_color())

        self.part_of_answer = IntVar(value=1)
        self.display_open = False
        self.question_number = question_number

        self.header = Frame(self, bg=StyledTkinter.get_medium_color())
        self.toggle_text = StringVar(value="+")
        self.toggle_display = StyledTkinter.get_dark_button(self.header,
                                                            textvariable=self.toggle_text,
                                                            command=self.toggle_input_display,
                                                            width=2)
        self.head_text_container = Frame(self.header,
                                         bg=StyledTkinter.get_medium_color(),
                                         highlightcolor=StyledTkinter.get_dark_color(),
                                         highlightthickness=1,
                                         highlightbackground=StyledTkinter.get_dark_color())
        self.header_title = Label(self.head_text_container,
                                  bg=StyledTkinter.get_medium_color(),
                                  text="Question " + str(question_number + 1))
        self.header_is_in_solution_indicator = Label(self.head_text_container,
                                                     text="In Solution",
                                                     bg=StyledTkinter.get_medium_color())

        self.question_frame = Frame(self, bg=StyledTkinter.get_medium_color())
        self.question_title_row = Frame(self.question_frame, bg=StyledTkinter.get_medium_color())
        self.question_in_solution = Checkbutton(self.question_title_row,
                                                text='Use in solution',
                                                variable=self.part_of_answer,
                                                bg=StyledTkinter.get_medium_color(),
                                                command=self.update_is_in_solution_indicator)
        self.question_label = Label(self.question_title_row, bg=StyledTkinter.get_medium_color(), text="Question")
        self.question = RichTextInput(self.question_frame)

        self.answer_tabs = TabContainer(self)

        answer_frame = self.answer_tabs.create_empty_tab("Answer")
        self.answer = RichTextInput(answer_frame)

        self.fillers = []
        for i in range(3):
            answer_frame = self.answer_tabs.create_empty_tab("Filler " + str(i + 1))
            self.fillers.append(RichTextInput(answer_frame))

        self.load(load_data)

    def update_is_in_solution_indicator(self):
        if self.part_of_answer.get():
            self.header_is_in_solution_indicator.config(text="In Solution")
        else:
            self.header_is_in_solution_indicator.config(text="")

    def display(self):
        super().pack(expand=True, fill=X)

        self.header.pack(expand=True, fill=X, pady=(5, 5))
        self.toggle_display.pack(side=LEFT)
        self.head_text_container.pack(side=LEFT, expand=True, fill=BOTH)
        self.header_title.pack(side=LEFT, padx=(0, 5), expand=True, fill=X)
        self.header_is_in_solution_indicator.pack(side=LEFT, padx=(0, 5), expand=True, fill=X)

        self.question_title_row.pack(expand=True, fill=X)
        self.question_label.pack(side=LEFT, padx=(0, 5), pady=(0, 5))
        self.question_in_solution.pack(side=LEFT, padx=(0, 5), pady=(0, 5))
        self.question.display(expand=True, fill=X)

        self.answer.display(expand=True, fill=X)
        for filler in self.fillers:
            filler.display(expand=True, fill=X)

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
        self.question_frame.pack(side=LEFT, expand=True, fill=X, padx=(0, 4))
        self.answer_tabs.display(side=LEFT, expand=True, fill=X)

        self.toggle_text.set("-")
        self.display_open = True

        PyBus.Instance().post(CloseOtherInputs(self.question_number))

    def close_input_display(self):
        self.question_frame.forget()
        self.answer_tabs.forget()
        self.toggle_text.set("+")
        self.display_open = False

    def load(self, load_data):
        if load_data is not None:
            self.part_of_answer.set(load_data['part_of_answer'])
            self.question.load_content(load_data['question'])
            self.answer.load_content(load_data['answer'])

            for filler in load_data['fillers']:
                index = load_data['fillers'].index(filler)
                self.fillers[index].load_content(filler)

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
            'part_of_answer': self.part_of_answer.get(),
            'question': self.question.get_content(),
            'answer': self.answer.get_content(),
            'fillers': [x.get_content() for x in self.fillers]
        }
