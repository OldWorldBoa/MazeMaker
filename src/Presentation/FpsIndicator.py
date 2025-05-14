import time

from tkinter import Text, END, RIGHT


class FpsIndicator:
    def __init__(self, master):
        self.textBox = Text(master, height=1, width=8)
        self.fpsStart = time.time()
        self.current_fps = 0
        self.last_tick_num = 0

    def pack(self):
        self.textBox.pack(side=RIGHT)
        self.textBox.insert(END, "...")

    def update_fps(self, tick_num):
        now = time.time()
        if now > self.fpsStart + 1:
            if self.last_tick_num == 0:
                self.last_tick_num = tick_num
                self.fpsStart = now
            else:
                self.current_fps = (tick_num - self.last_tick_num) / (now - self.fpsStart)
                self.textBox.delete('1.0', END)
                self.textBox.insert(END, f"{self.current_fps:.2f}fps")

                self.last_tick_num = tick_num
                self.fpsStart = now
