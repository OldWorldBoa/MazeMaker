# Dependencies
- pip install pyeventbus3
    - event bus for commands
- pip install Pillow 
    - export canvas as jpg
- pip install pytest
    - testing framework 
- [Ghostscript](https://www.ghostscript.com/download/gsdnld.html)
    - used with Pillow
  
# Build an exe
Run PyInstaller on the Main.py script like so:
```commandline
PyInstaller -F Main.py
```