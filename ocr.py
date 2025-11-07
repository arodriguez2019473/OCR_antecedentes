# ingatumare ad ocr module
# ya me enoje >:(
# si ves esto, felicidades, has encontrado un easter egg
from PIL import Image

import pytesseract
import pdf2image
# import traceback
import re

def borrado_texto(text):
    
    # aca va la funcion de borrado de texto sensible 
    lines = text.split('\n')
    # lines es una lista de strings es una variable temporal si quieres le cambias el nombre pa que trueene mas sentido
    # para sacar este simbolo raro \ se presiona las teclas alt + 92
    borrado_lines = []

    # esto que hare lo vi en un video de youtube y starkoverflow
    for line in lines:
        
        line = line.strip()
        if len(line)< 2:
            continue
            # continue es para saltarse la iteracion actual y pasar a la siguiente como tu ex cuando te veia y no queria hablarte 
        
        special_char_ratio =( sum(
            not c.isalnum()
            and not c.isspace()
            for c in line) / len(line) #<---- ojo aca cerramos el sum no estes 30 minutos como yo buscando el error

            if line else 0 
            # esto es por si la linea esta vacia para evitar division por cero
        )
        
        if special_char_ratio > 0.5:
            continue    

        # que hice ahi
        # pues basicamente contamos cuantos caracteres especiales hay en la linea y lo dividimos entre la longitud de la linea
        # asi obtenemos un ratio de caracteres especiales
        # ejemplo de bebe si tu ex te hablaba 10 veces al dia y 5 de esas veces eran para pedirte dinero
        # el ratio de veces que te hablaba para pedir dinero era de 5/10
        # si el ratio es mayor a 0.5 (50%) entonces consideramos que la linea tiene mucho texto sensible y la borramos de nuestra vida ella no vale la pena  
        # pero si te hablaba 2 veces al dia y solo 1 de esas veces era para pedirte dinero
        # era bien confiable tu ex y no la borrabas de tu vida
        # pero aun asi no vuelvas con ella
        
        if len(set(line.replace(" ",""))) <= 3 and len(line) > 5:
            continue
        # aca ya vemos que ella no vale la pena
        # si la linea tiene 5 o mas caracteres y solo tiene 3 caracteres unicos o menos
        # entonces la borramos de nuestra vida a chingar a su madre
        
        borrado_lines.append(line)

    return '\n'.join(borrado_lines)
    # para mejor explicacion preguntale alguna ia como chatgpt o bard

def procesar_pdf(pdf_path):
    # vamos a convertir el pdf en imagenes el codigo lo saque de la documentacion de pdf2image
    # https://pdf2image.readthedocs.io/en/latest/
    # y una ayudadita de ias XD
    
    try:
        images = pdf2image.convert_from_path(pdf_path, dpi=300)
        extracted_text = ""

        for i, image in enumerate(images, 1):
            
            try:
                text = pytesseract.image_to_string(image, lang='spa', config='--psm 6')
            except Exception:
                text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')

            text = borrado_texto(text)

            if text.strip():
                extracted_text += f"\n--- página {i} ---\n{text}\n"

        return extracted_text, None

    except Exception as e:
        return "", "pa error al procesar el pdf"

# el try except es para manejar errores
# si algo sale mal en el bloque try
# este wey lo va a agarrar y ejecutar el bloque except
# es como tu amigo que te dice que tu ex no vale la pena cuando estas triste
# y te ayuda a seguir adelante sin llorar por ella

def verificar(texto):
    # al chile no se que hacer aqui
    # asi que solo voy a poner una funcion que verifique si hay antecedentes o no

    texto = texto.upper()

    # esto pondre por que lei por ahi que hay que poner tildes para verificar bien

    texto = re.sub(r"[ÁÀÄÂ]", "A", texto)
    texto = re.sub(r"[ÉÈËÊ]", "E", texto)
    texto = re.sub(r"[ÍÌÏÎ]", "I", texto)
    texto = re.sub(r"[ÓÒÖÔ]", "O", texto)
    texto = re.sub(r"[ÚÙÜÛ]", "U", texto)
    
    # esto dicen por ahi que sirve para normalizar el texto por eso lo puse 

    if "—— NO TIENE ANTECEDENTES POLICIALES ——" in texto:
        return "no hay antecedentes "

    elif "*** NO LE APARECEN ANTECEDENTES PENALES ***" in texto:
        return "no tiene antecedentes"
    
    elif "TIENE ANTECEDENTES POLICIALES" in texto:
        return "tiene antecedentes"
    
    elif "TIENE ANTECEDENTES PENALES" in texto:
        return "tiene antecedentes"
    
    else: 
        return"posiblemente tiene antecedentes"
    
    # esto es bien basico pero ni siquiera te voy a explicar mamon 


def Datos(texto):

    # esto lo aprendi de choloma 
    
    texto = texto.upper()
    texto = re.sub(r"[ÁÀÄÂ]", "A", texto)
    texto = re.sub(r"[ÉÈËÊ]", "E", texto)
    texto = re.sub(r"[ÍÌÏÎ]", "I", texto)
    texto = re.sub(r"[ÓÒÖÔ]", "O", texto)
    texto = re.sub(r"[ÚÙÜÛ]", "U", texto)

    texto = re.sub(r"[áàäâ]", "a", texto)
    texto = re.sub(r"[éèëê]", "e", texto)
    texto = re.sub(r"[íìïî]", "i", texto)
    texto = re.sub(r"[óòöô]", "o", texto)
    texto = re.sub(r"[úùüû]", "u", texto)


    datos = {

        "nombres":str,
        "apellido":str,
        # "DPI":None,
        "CUI":None
    }

    nombres_antecedente = re.search(r"NOMBRES?\s*[:\-]?\s*([A-Z\s]+)", texto)
    apellidos_antecedente = re.search(r"APELLIDOS?\s*[:\-]?\s*([A-Z\s]+)", texto)
    dpi_antecedente = re.search(r"CUI\s*[:\-]?\s*(\d{4,})", texto)

    if nombres_antecedente:
        datos["nombres"] = nombres_antecedente.group(1).strip()

    if apellidos_antecedente:
        datos["apellido"] = apellidos_antecedente.group(1).strip()

    if dpi_antecedente:
        datos["CUI"] = dpi_antecedente.group(1).strip()

    return datos


