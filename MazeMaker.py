from tkinter import Tk, PhotoImage

from src.Business.Infrastructure.AppMediator import AppMediator

if __name__ == "__main__":
    root = Tk()
    root.state('zoomed')
    root.tk.call('encoding', 'system', 'unicode')

    photo = PhotoImage(file="./res/logo.png")
    root.iconphoto(False, photo)

    app = AppMediator(root)
    app.display()
    app.tick()

    root.mainloop()
