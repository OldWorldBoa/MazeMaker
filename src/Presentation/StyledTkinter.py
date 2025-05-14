from tkinter import Button, FLAT


class StyledTkinter:
    def __init__(self):
        pass

    @staticmethod
    def get_dark_button(master, *args, **kwargs):
        return Button(master, *args, **kwargs, relief=FLAT,
                      bg=StyledTkinter.get_dark_color(),
                      fg=StyledTkinter.get_light_color(),
                      activebackground="gray15",
                      activeforeground="gray63")

    @staticmethod
    def get_primary_color():
        return ""

    @staticmethod
    def get_accent_color():
        return ""

    @staticmethod
    def get_light_color():
        return "gray88"

    @staticmethod
    def get_dark_color():
        return "gray40"
