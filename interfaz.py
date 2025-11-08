import tkinter as tk
import os
import webbrowser

from tkinter import filedialog, messagebox, scrolledtext
from ocr import procesar_pdf, borrado_texto, verificar, Datos, guardar_en_excel, leer_qr_de_pdf
from config import configure_tesseract

class PDFOCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Texto PDF con OCR")
        self.root.geometry("700x600")

        # Configurar Tesseract
        configure_tesseract()

        # definimos aca unas variables bien locas no sabia que podia hacer eso xd

        self.texto_policial = None
        self.texto_penal = None
        self.datos_persona = None 

        # Crear interfaz
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            main_frame, text="Extractor de Texto de PDF",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # self.select_button = tk.Button(
        #     main_frame,
        #     text="📄 Seleccionar archivo PDF",
        #     command=self.select_pdf,
        #     font=("Arial", 12),
        #     bg="#4CAF50",
        #     fg="white",
        #     padx=20,
        #     pady=10,
        #     cursor="hand2"
        # )
        
        self.btn_policial = tk.Button(
            main_frame,
            text="📄 Subir Antecedentes POLICIALES",
            command=self.cargar_policiacos,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.btn_policial.pack(pady=10)

        self.btn_penal = tk.Button(
            main_frame,
            text="📄 Subir Antecedentes PENALES",
            command=self.cargar_penales,
            font=("Arial", 12),
            bg="#FF5722",
            fg="white",
            padx=20,
            pady=10
        )
        self.btn_penal.pack(pady=10)


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

# aca hay pura logica ahuevo

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

        # Procesar el PDF (OCR)
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

            # Verificar antecedentes automáticamente
            resultado = verificar(extracted_text)
            self.text_area.insert(tk.END, f"\n\n--- Resultado de verificación ---\n{resultado}")
            messagebox.showinfo("Verificación completada", resultado)

            # Extraer datos (Nombre, Apellido, CUI)
            info = Datos(extracted_text)
            print(info)

            # Leer QR desde el PDF
            qr_data = leer_qr_de_pdf(self.pdf_path)

            if qr_data:
                webbrowser.open(qr_data)  # Abre navegador para validad
                estado_validacion = "Pendiente de verificación manual"
            else:
                estado_validacion = "No se encontró QR"

            # Guardar datos en Excel
            guardar_en_excel({
                "Nombres": info.get("nombres"),
                "Apellidos": info.get("apellido"),
                "CUI": info.get("CUI"),
                "QR": qr_data,
                "Resultado OCR": resultado,
                "Validación": estado_validacion
            })

            messagebox.showinfo("Guardado", "Datos guardados en Excel ✅")

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

    def cargar_policiacos(self):
        
        file_path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf*")])

        if not file_path:
            
            return

        texto, err = procesar_pdf(file_path)
        
        if err:
        
            messagebox.showerror("Error we", err)
            return

        self.texto_policial = texto
        self.datos_persona = Datos(texto)

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "Antecedentes policiacos cargados \n\n")
        self.text_area.insert(tk.END, texto)
        
        print("\n datos extraidos(Policiales)")
        print(self.datos_persona)
        print("_______________________________")

    def cargar_penales(self):
        
        file_path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf*")])
        
        if not file_path:
            return
        
        texto, err = procesar_pdf(file_path)

        if err:
            
            messagebox.showerror("Error en algo", err)
            return

        self.texto_penal = texto

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "antecedentes penales cargados\n\n")
        self.text_area.insert(tk.END, texto)

        self.verificar_todo()

    
    # ahora si se viene lo divertido verificar todo alv

    def verificar_todo(self):

        if not self.texto_policial or not self.texto_penal:
            messagebox.showwarning("Falta archivos","suba los dos archivos antes de extraer datos")
            
            return
        
        resultado_policiaco = verificar(self.texto_penal)
        resultado_penal = verificar(self.texto_policial)

        
        self.text_area.insert(tk.END, "\n\n--- RESULTADO FINAL ---\n")
        self.text_area.insert(tk.END, f"Antecedentes Policiales: {resultado_policiaco}\n")
        self.text_area.insert(tk.END, f"Antecedentes Penales: {resultado_penal}\n\n")

        self.text_area.insert(tk.END, f"Nombres: {self.datos_persona.get('nombres', 'No detectado')}\n")
        self.text_area.insert(tk.END, f"Apellidos: {self.datos_persona.get('apellido', 'No detectado')}\n")
        self.text_area.insert(tk.END, f"CUI: {self.datos_persona.get('CUI', 'No detectado')}\n")

        print("\n✅ VERIFICACIÓN COMPLETA")
        print("Policiales:", resultado_policiaco)
        print("Penales:", resultado_penal)
        print("Datos:", self.datos_persona)
        print("--------------------------------------------")


    