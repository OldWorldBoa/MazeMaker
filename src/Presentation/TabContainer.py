from .StyledTkinter import StyledTkinter
from .Menu import Menu

from tkinter import Frame, BOTH, NSEW


class TabContainer(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.selected_index = 0
        self.tab_menu = Menu(self, bg=StyledTkinter.get_medium_color())
        self.tab_content_container = Frame(self)
        self.tabs = []

    def create_empty_tab(self, title):
        new_index = len(self.tabs)
        self.tab_menu.add_button(title, lambda: self.set_active_tab(new_index))

        tab = Frame(self.tab_content_container)
        self.tabs.append(tab)

        return tab

    def set_active_tab(self, index):
        for tab in self.tabs:
            tab.grid_remove()

        self.tabs[index].grid(row=0, column=0, sticky=NSEW)

    def display(self, **kwargs):
        super().grid(TabContainer.get_display_options(**kwargs))

        self.tab_menu.display()
        self.tab_content_container.pack(expand=True, fill=BOTH)

        self.set_active_tab(0)

    @staticmethod
    def get_display_options(**kwargs):
        if "column" not in kwargs:
            kwargs["column"] = 0

        if "sticky" not in kwargs:
            kwargs["sticky"] = NSEW

        return kwargs
