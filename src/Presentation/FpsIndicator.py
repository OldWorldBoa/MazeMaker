import time
from decimal import Decimal
from tkinter import Text, Tk, END, RIGHT

class FpsIndicator():
  def __init__(self, master):
    self.textBox = Text(master, height=1, width=8)
    self.fpsStart = time.time()
    self.currentFps = 0
    self.lastTicknum = 0

  def pack(self):
    self.textBox.pack(side=RIGHT)
    self.textBox.insert(END, "...")

  def updateFps(self, tickNum):
    now = time.time()
    if now > self.fpsStart + 1:
      if self.lastTicknum == 0: 
        self.lastTicknum = tickNum
        self.fpsStart = now
      else:
        self.currentFps = (tickNum - self.lastTicknum) / (now - self.fpsStart)
        self.textBox.delete('1.0', END)
        self.textBox.insert(END, f"{self.currentFps:.2f}fps")

        self.lastTicknum = tickNum
        self.fpsStart = now
