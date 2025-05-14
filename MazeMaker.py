from tkinter import Tk

from src.Business.Infrastructure.AppMediator import AppMediator

if __name__ == "__main__":
    root = Tk()
    root.state('zoomed')

    app = AppMediator(root)
    app.pack()
    app.tick()

    root.mainloop()
