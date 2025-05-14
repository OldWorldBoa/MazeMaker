from ..Menu import Menu
from ...Business.Tools.DrawMazeTool import DrawMazeTool
from ...Business.Events.SelectToolEvent import SelectToolEvent
from ...Business.Events.ChangeQuestionWidth import ChangeQuestionWidth
from ...Business.Events.ChangeQuestionHeight import ChangeQuestionHeight
from ...Business.Events.ChangeAnswerLength import ChangeAnswerLength
from ...Business.Events.ChangeAnswerWidth import ChangeAnswerWidth

from pyeventbus3.pyeventbus3 import *
from tkinter import Label, StringVar, LEFT


# The click button command handlers require one parameter,
# but it isn't currently used so we are ignoring the following:
# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyMethodParameters
class GraphRendererMenu(Menu):
    def __init__(self, master, question_height, question_width, answer_length, answer_width):
        super().__init__(master)

        self.master = master
        self.add_button("Draw Maze", self.click_draw_maze)
        self.add_entry("Question Height: ", question_height, self.change_question_height)
        self.add_entry("Question Width: ", question_width, self.change_question_width)
        self.add_entry("Answer Length: ", answer_length, self.change_answer_length)
        self.add_entry("Answer Width: ", answer_width, self.change_answer_width)

    def click_draw_maze(click_event):
        PyBus.Instance().post(SelectToolEvent(DrawMazeTool()))

    def change_question_height(self, new_height):
        PyBus.Instance().post(ChangeQuestionHeight(new_height))

    def change_question_width(self, new_width):
        PyBus.Instance().post(ChangeQuestionWidth(new_width))

    def change_answer_length(self, new_length):
        PyBus.Instance().post(ChangeAnswerLength(new_length))

    def change_answer_width(self, new_width):
        PyBus.Instance().post(ChangeAnswerWidth(new_width))
