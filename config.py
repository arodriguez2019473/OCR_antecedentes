import os 
import sys
import pytesseract
from tkinter import messagebox

# vamos a configurar la ruta de tesseract
# la ruta puede variar dependiendo de donde lo hayas instalado

def configure_tesseract():
    """Busca Tesseract en ubicaciones comunes y lo configura."""
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Tesseract-OCR\tesseract.exe",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return

    if sys.platform == "win32":
        messagebox.showwarning(
            "Tesseract no encontrado",
            "No se encontró Tesseract-OCR.\n\n"
            "Descárgalo desde:\n"
            "https://github.com/UB-Mannheim/tesseract/wiki\n\n"
            "Durante la instalación selecciona el idioma 'Spanish'."
        )

# esto si utilice ia para hacerlo mas rapido