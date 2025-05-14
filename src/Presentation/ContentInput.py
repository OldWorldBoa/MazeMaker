from tkinter import Frame, Entry, Label


class ContentInput(Frame):
    def __init__(self, master):
        super().__init__(master, bg="gray75")

        self.question_label = Label(self, bg="gray75", text="Question")
        self.question = Entry(self)
        self.answer_label = Label(self, bg="gray75", text="Answer")
        self.answer = Entry(self)

    def grid(self, **kwargs):
        super().grid(kwargs, sticky="new")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

        self.question_label.grid(row=0, column=0, sticky="new")
        self.question.grid(row=0, column=1, padx=(0, 20), sticky="new")
        self.answer_label.grid(row=0, column=2, sticky="new")
        self.answer.grid(row=0, column=3, sticky="new")

    def is_filled(self):
        if self.question.get() != "" and self.answer.get() != "":
            return True

        return False

    def get_as_dict(self):
        return {'question': self.question.get(), 'answer': self.answer.get()}
