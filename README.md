# OCR Screenshot Tool

A simple Python desktop application that captures a screenshot, sends it to the Google Cloud Vision API for OCR, and displays the extracted text in a popup window.

## Features

* Capture full-screen screenshots.
* Extract text using Google Cloud Vision API.
* Display results in a GUI popup (Tkinter).
* Configure via a `.env` file.
* Bundle as a standalone Windows executable using PyInstaller.

## Prerequisites

* **Python 3.7+**
* A valid Google Cloud API key for Vision API.
* (Windows only) **PyInstaller** for building the executable.

## Setup

1. **Clone or download** this repository to your local machine.
2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Create a `.env` file** in the project root with the following content:

   ```dotenv
   GOOGLE_API_KEY=YOUR_VISION_API_KEY_HERE
   ```

## Usage

### Running with Python

From the project directory, execute:

```bash
python extract.py
```

A popup window will appear displaying the extracted text from your screen.

### Building the Executable

1. Install PyInstaller if you haven't already:

   ```bash
   pip install pyinstaller
   ```
2. Build the standalone executable:

   ```bash
   pyinstaller --onefile --windowed --add-data ".env;." --name ocr_screenshot extract.py
   ```
3. Locate your executable in the `dist/` folder:

   ```
   dist/ocr_screenshot.exe
   ```

## Configuration Loading in Executable

The script includes logic to load the `.env` file both in normal execution and when frozen by PyInstaller:

```python
import os
import sys
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)

dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)
```

## Troubleshooting

* **`Missing GOOGLE_API_KEY`**: Ensure your `.env` file is named exactly `.env` and placed in the same directory as the script or the bundled executable.
* **Missing modules in executable**: Use the `--hidden-import` flag or modify the generated `.spec` file to include necessary modules.
* **`.env` not loaded**: Verify that you included `--add-data ".env;."` in the PyInstaller command and that the code references `sys._MEIPASS` correctly.

## requirements.txt

```text
google-cloud-vision
python-dotenv
pillow
mss
```

Tkinter is included with most Python installations and does not need to be added.

## License

This project is licensed under the MIT License.

## Acknowledgements

* [Google Cloud Vision API](https://cloud.google.com/vision)
* [python-dotenv](https://github.com/theskumar/python-dotenv)
* [PyInstaller](https://www.pyinstaller.org/)
