# ingatumare ad ocr module
# ya me enoje >:(
# si ves esto, felicidades, has encontrado un easter egg

from PIL import Image

import pytesseract
import pdf2image
import traceback

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
        
        special_char_ratio = sum(
            not c.isalnum()
            and not c.isspace()
            for c in line) / len(line) #<---- ojo aca cerramos el sum no estes 30 minutos como yo buscando el error
            
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
        
        if len(set(line.replace("",""))) <= 3 and len(line) > 5:
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
            
            text = pytesseract.image_to_string(image, lang='spa', config='--psm 6')

            text = borrado_texto(text)

            if text.strip():
                extracted_text += "\n--- pagina {i} ----\n {text}\n"

        return extracted_text, None

    except Exception as e:
        return "", "pa error al procesar el pdf"

# el try except es para manejar errores
# si algo sale mal en el bloque try
# este wey lo va a agarrar y ejecutar el bloque except
# es como tu amigo que te dice que tu ex no vale la pena cuando estas triste
# y te ayuda a seguir adelante sin llorar por ella
