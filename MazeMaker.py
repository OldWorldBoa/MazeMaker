from tkinter import Tk

from src.Business.Infrastructure.AppMediator import AppMediator

if __name__ == "__main__":
    root = Tk()
    root.state('zoomed')

    app = AppMediator(root)
    app.display()
    app.tick()

    root.mainloop()
