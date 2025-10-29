import tkinter as tk
import os

from tkinter import filedialog, messagebox, scrolledtext
from ocr import procesar_pdf, borrado_texto
from config import configure_tesseract

class PDFOCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Texto PDF con OCR")
        self.root.geometry("700x600")

        # Configurar Tesseract
        configure_tesseract()

        # Crear interfaz
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            main_frame, text="Extractor de Texto de PDF",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        self.select_button = tk.Button(
            main_frame,
            text="📄 Seleccionar archivo PDF",
            command=self.select_pdf,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.select_button.pack(pady=10)

        self.file_label = tk.Label(
            main_frame, text="Ningún archivo seleccionado",
            font=("Arial", 10), fg="gray"
        )
        self.file_label.pack(pady=5)

        self.process_button = tk.Button(
            main_frame,
            text="🔍 Extraer texto (OCR)",
            command=self.procesar_pdf,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.process_button.pack(pady=10)

        result_label = tk.Label(
            main_frame, text="Texto extraído:",
            font=("Arial", 11, "bold")
        )
        result_label.pack(pady=(20, 5), anchor="w")

        self.text_area = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD,
            width=70, height=20,
            font=("Arial", 10)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(
            main_frame,
            text="💾 Guardar texto",
            command=self.save_text,
            font=("Arial", 10),
            bg="#FF9800",
            fg="white",
            padx=15,
            pady=8,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.save_button.pack(pady=(10, 0))

        self.pdf_path = None

    # ==== FUNCIONES GUI ====

    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Seleccione un archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.pdf_path = file_path
            file_name = os.path.basename(file_path)
            self.file_label.config(text=f"Archivo: {file_name}", fg="black")
            self.process_button.config(state=tk.NORMAL)
            self.text_area.delete(1.0, tk.END)
            self.save_button.config(state=tk.DISABLED)

    def procesar_pdf(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Por favor seleccione un archivo PDF primero")
            return

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Procesando PDF... Por favor espere...\n")
        self.root.update()

        extracted_text, error_msg = procesar_pdf(self.pdf_path)

        self.text_area.delete(1.0, tk.END)
        if error_msg:
            messagebox.showerror("Error", error_msg)
            self.text_area.insert(tk.END, error_msg)
            return

        if extracted_text.strip():
            self.text_area.insert(tk.END, extracted_text)
            self.save_button.config(state=tk.NORMAL)
            messagebox.showinfo("Éxito", "Texto extraído correctamente")
        else:
            self.text_area.insert(tk.END, "No se encontró texto legible en el PDF.")

    def save_text(self):
        text_content = self.text_area.get(1.0, tk.END)
        if not text_content.strip():
            messagebox.showwarning("Advertencia", "No hay texto para guardar")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            messagebox.showinfo("Éxito", "Texto guardado correctamente")


# tenia pereza de escribir todo esto xd
# lo hice con ia
# claro ya que lo revise y edite un poco para que quedara a mi gusto