# aca va a ser el punto de arranque de la aplicacion
# lo hago pa que se vea mas profesional / mas vrg creo

from interfaz import PDFOCRApp
from selenium import webdriver

import tkinter as tk
import webbrowser

def main():
    
    # print("Iniciando la aplicacion...")
    # print("Aplicacion iniciada correctamente.")

    root = tk.Tk()
    app = PDFOCRApp(root) #<-- XD puse pedrocraftapp ajajajajaja
    root.mainloop()

if __name__ == "__main__":
    main()

