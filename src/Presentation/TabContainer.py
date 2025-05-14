from .StyledTkinter import StyledTkinter
from .Menu import Menu

from tkinter import Frame, X, RAISED


class TabContainer(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.selected_index = 0
        self.tab_menu = Menu(self, bg=StyledTkinter.get_medium_color())
        self.tab_content_container = Frame(self, relief=RAISED, borderwidth=3, bg=StyledTkinter.get_medium_color())
        self.tabs = []

    def create_empty_tab(self, title):
        new_index = len(self.tabs)
        self.tab_menu.add_button(title, lambda: self.set_active_tab(new_index))

        tab = Frame(self.tab_content_container, bg=StyledTkinter.get_medium_color())
        self.tabs.append(tab)

        return tab

    def display(self, **kwargs):
        super().pack(kwargs)

        self.tab_menu.display()
        self.tab_content_container.pack(expand=True, fill=X)

        self.set_active_tab(0)

    def set_active_tab(self, index):
        for tab in self.tabs:
            tab.forget()

        for button in self.tab_menu.elements:
            btn_index = self.tab_menu.elements.index(button)

            if btn_index == index:
                button.configure(fg="black")
                button.configure(bg="white")
            else:
                button.configure(fg=StyledTkinter.get_light_color())
                button.configure(bg=StyledTkinter.get_dark_color())

        self.tabs[index].pack(expand=True, fill=X)

    @staticmethod
    def get_display_options(**kwargs):
        if "column" not in kwargs:
            kwargs["column"] = 0

        if "row" not in kwargs:
            kwargs["row"] = 0

        return kwargs
