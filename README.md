# PDFAutoCropper
Python GUI tool for automatically batch-cropping PDF pages

## Dependencies
Runs on Python 2.7 onwards. Requires `PyPDF2` and `gooey`, which can be installed via pip:

     pip install PyPDF2
     pip install gooey
     
Should work on Windows, macOS and Linux, provided Python and above dependencies are available and installed.

## Running
Script can be called without any arguments, the GUI will then appear for configuration:

     python pdfCropper.py

## Building Executable
A PyInstaller `build.spec` file is included that configures PyInstaller to build and package a stand-alone executable file. This requires PyInstaller to be available:

     pip install pyinstaller

The executable can then be built:

     pyinstaller build.spec
