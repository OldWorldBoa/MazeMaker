from pyeventbus3.pyeventbus3 import *

from ..Tools.Tool import Tool
from ..Events.SelectToolEvent import SelectToolEvent

class KeyPressHandler():
  def __init__(self, master):
    master.bind('<KeyPress>', self.onKeyPress)

  def onKeyPress(self, event):
    if (event.keycode == 27):
      PyBus.Instance().post(SelectToolEvent(Tool()))