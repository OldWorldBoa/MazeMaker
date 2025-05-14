from ..Menu import Menu
from ..NumericEntry import NumericEntry
from ...Business.Tools.DrawMazeTool import DrawMazeTool
from ...Business.Events.SelectToolEvent import SelectToolEvent
from ...Business.Events.ChangeQuestionWidth import ChangeQuestionWidth
from ...Business.Events.ChangeQuestionHeight import ChangeQuestionHeight
from ...Business.Events.ChangeAnswerLength import ChangeAnswerLength
from ...Business.Events.ChangeAnswerWidth import ChangeAnswerWidth
from ...Business.Events.ToggleSolutionView import ToggleSolutionView

from pyeventbus3.pyeventbus3 import *
from tkinter import DISABLED, NORMAL, Tk, StringVar


# The click button command handlers require one parameter,
# but it isn't currently used so we are ignoring the following:
# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyMethodParameters
class GraphRendererMenu(Menu):
    def __init__(self, master, question_height, question_width, answer_length, answer_width):
        super().__init__(master)

        self.master = master

        self.question_height_key = "QHK"
        self.question_width_key = "QWK"
        self.answer_length_key = "ALK"
        self.answer_width_key = "AWK"
        self.entries = {}

        self.add_button("Edit Maze Size", lambda: self.click_edit_maze_size())
        self.add_debounced_button("Show Solution", lambda: self.click_show_solution())
        self.add_entry("Question Height: ", self.create_numeric_entry(self.question_height_key,
                                                                      question_height,
                                                                      self.change_question_height))

        self.add_entry("Question Width: ", self.create_numeric_entry(self.question_width_key,
                                                                     question_width,
                                                                     self.change_question_width))

        self.add_entry("Answer Length: ", self.create_numeric_entry(self.answer_length_key,
                                                                    answer_length,
                                                                    self.change_answer_length))

        self.add_entry("Answer Width: ", self.create_numeric_entry(self.answer_width_key,
                                                                   answer_width,
                                                                   self.change_answer_width))

    def create_numeric_entry(self, key, initial_value, callback):
        value_container = StringVar()
        value_container.trace_add("write", lambda x, y, z: callback(value_container.get()))

        self.entries[key] = value_container

        return NumericEntry(self, initial_value, width=5, textvariable=value_container)

    def update_question_height(self, new_val):
        self.entries[self.question_height_key].set(new_val)

    def update_question_width(self, new_val):
        self.entries[self.question_width_key].set(new_val)

    def update_answer_length(self, new_val):
        self.entries[self.answer_length_key].set(new_val)

    def update_answer_width(self, new_val):
        self.entries[self.answer_width_key].set(new_val)

    def display(self, **kwargs):
        super().display(pady=(5, 5), padx=(5, 0))

    def click_edit_maze_size(self):
        PyBus.Instance().post(SelectToolEvent(DrawMazeTool()))

    def click_show_solution(self):
        show_solution_button = self.elements[1]
        show_solution_button['state'] = DISABLED
        Tk.update(self.master)

        curr_text = show_solution_button['text']
        if curr_text == "Show Solution":
            show_solution_button['text'] = "Hide Solution"
        else:
            show_solution_button['text'] = "Show Solution"

        PyBus.Instance().post(ToggleSolutionView())
        time.sleep(0.2)
        show_solution_button['state'] = NORMAL

    def change_question_height(self, new_height):
        PyBus.Instance().post(ChangeQuestionHeight(new_height))

    def change_question_width(self, new_width):
        PyBus.Instance().post(ChangeQuestionWidth(new_width))

    def change_answer_length(self, new_length):
        PyBus.Instance().post(ChangeAnswerLength(new_length))

    def change_answer_width(self, new_width):
        PyBus.Instance().post(ChangeAnswerWidth(new_width))
