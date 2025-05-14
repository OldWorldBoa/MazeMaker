from tkinter import Tk

from src.Business.Infrastructure.AppMediator import AppMediator

if __name__ == "__main__":
    root = Tk()
    root.geometry("700x600")

    app = AppMediator(root)
    app.pack()
    app.tick()

    root.mainloop()
