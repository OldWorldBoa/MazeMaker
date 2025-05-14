from tkinter import Button, FLAT


class StyledTkinter:
    def __init__(self):
        pass

    @staticmethod
    def get_styled_button(master, *args, **kwargs):
        return Button(master, *args, **kwargs, relief=FLAT,
                      bg="gray40", fg="gray88", activebackground="gray15",
                      activeforeground="gray63")
