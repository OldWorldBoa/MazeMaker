# Installation
Download the [latest version](https://drive.google.com/uc?id=1D9o52jChc9EKH1Ec2zxtuO2BxzzAwUEs&export=download)
or clone the repo and build an exe yourself!

### Previous Versions

* [v1](https://drive.google.com/uc?id=1TMQoJ9FiQthlucI9lzC3EAXUf3-PJIf7&export=download)

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
Run one of these PyInstaller commands (rls for no console):
```commandline
PyInstaller MazeMaker.rls.spec
PyInstaller MazeMaker.spec
```

# Quick Start
1. Click "Draw Maze" in the second visible menu- then drag your cursor onto the main
   canvas. Click to persist.
2. In the top menu, click "Edit Content".
3. Expand each question, filling in the question, answer, and fillers.
   - Alternatively, click the "Fill with test data" button if you just want to see how
     it works!
4. Click "Generate Maze" at the top of the content editing column.
5. You now have a maze, congratulations!

## Extras
1. The print button will automatically print the maze with and without the solution.
   - Printing is very simple right now. If you need more control with how it prints,
     print to a PDF and then use your favorite PDF editor to print with more control.
     You can also export to a jpg and use that in other documents which you can print
     from their editors.
2. The export button doesn't export both the original and the solution. You have to
   export them separately with the "Show Solution" button.
3. Look at the bottom right for messages if you're not sure what's happening. Some
   error messages appear there.