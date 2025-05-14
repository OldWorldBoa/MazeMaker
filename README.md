# Dependencies
- pip install pywin32
  - for printing straight to the printer 
- pip install pyeventbus3
  - event bus for commands
- pip install pytest
  - testing framework
- pip install opencv-python
  - used to trim images to correct sizes
- pip install img2pdf
  - pdf conversion with no visual artifacts
- pip install Pillow 
  - export canvas as jpg
- [Ghostscript](https://www.ghostscript.com/download/gsdnld.html)
  - used with Pillow
  - this is in the lib folder; no install necessary
- To print, a pdf reader needs to be installed and set as the default program to print pdfs
  - [Bullzip PDF Studio](https://www.bullzip.com/products/stu/), for example
  - The setting "Let Windows manage my default printer" must be off
  
# Build an exe
Run PyInstaller on the Main.py script like so:
```commandline
PyInstaller -F Main.py
```