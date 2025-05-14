import io

from PIL import Image
from tkinter import filedialog

from .Tool import Tool

class ExportTool(Tool):
  def __init__(self):
    pass

  def run(self, command, **kwargs):
    if (command == "EXECUTE"): 
      file = filedialog.asksaveasfilename(defaultextension=".jpg")
      canvas = kwargs["canvas"]
      ps = canvas.postscript(colormode = 'color')
      im = Image.open(io.BytesIO(ps.encode('utf-8')))
      im.save(file + '.jpg')