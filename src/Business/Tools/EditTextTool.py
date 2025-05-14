from .Tool import Tool

class EditTextTool(Tool):
	def __init__(self):
		pass

  def mouseClick(self, event):
    PyBus.Instance().post(EditTextAt(event.x, event.y))