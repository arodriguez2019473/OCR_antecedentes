import easyocr
# si no tienes la libreria instalada, usa: pip install easyocr pillow a pq si no la tienes no jala el codigo que pendejo
# esta libreria nos servira para poder leer el texto de la imagen

from pdf2image import convert_from_path
# esto me lo saque de un video de youtube XD
# a tambien es una libreria que convierte pdfs en imagenes
# esto lo voy a meter en el aplicativo pa que ya no lo instalen externamente

from io import BytesIO
# entonces importamos bytesio para manejar las imagenes en memoria

from PIL import Image
# utilizamos a pilow para el manejo de imagenes y poder utilizarlas en el easyocr ahuevo


reader = easyocr.Reader(['es'])
# https://www.jaided.ai/easyocr/tutorial/ ---> aqui esta la documentacion de easyocr esta en ingles aprende ingles wey

# ahora aca ni idea que hacer a futuro XD
pdf_path = "rutabienendeja alv.pdf"

pages = convert_from_path(pdf_path)
# ahora convierto a tu jefa en imagenes
# sigueme en mis canales oficiales de twitch y youtube :v que no tengo XD

texts = ""
#  esta madre va a guardar el peso de tu jefa osea el texto extraido de la imagen
# osea si estas bien wey es una variable vacia tambien se puede cambiar a una lista pero ya despues lo uno si me da ganas
# me acabo de fijar que la variable lo podia poner primero y despues el for pero ya ni modo wey 
# que lo arregle el senior
# a nms yo soy el senior aqui XD

for i, page in enumerate(pages):
    # pa que no digas que no soy culero aca te explico cabron
    # aqui recorremos cada pagina que se convirtio en imagen por que podes estar bien wey y tener un pdf
    # de 100 paginas y pues no voy a leer solo la primera wey no tamos pendejos o si no se
    # bueno ya me perdi wey
    # a si el enumerate es para que me de el indice de la pagina por si quiero guardarla o algo
    # no es necesario pero pues ya lo puse wey yo soy asi de chido
    
    print(f"Procesando la pagina - {i+1}")
    # esto es para que la gente vea que soy chido y que si le se y funcione 
    # ademas de que asi saben en que pagina va el proceso
    # es mi console en vivo cabron capo master papu amen

    pages.save("temp_page.jpg", "PNG")
    # guardamos la pagina temporalmente con el formato de png osea tus jefas
    # no le pongo al temp_page otro nombre por que luego se me hace un desmadre wey y yo toy bien menso
    
    result = reader.readtext("temp_page.jpg")
    # ahora si leemos a tu jefa con easyocr wey si no entendiste nada de lo de arriba wey
    # aqui guardamos el resultado en una variable llamada result y lo leemos con el reader que es
    # el easyocr que inicializamos arriba awebo, ni yo me entiendo haste grande preguntale a chatgpt wey o a mi mama

    for (_, text, fe ) in result:
        texts += text + " "

    # te preguntas que hice aqui wey?
    # pues recorri el resultado que me dio easyocr y saque solo el texto
    # el resultado es una lista de tuplas donde cada tupla tiene 3 elementos
    # el primero es la posicion del texto en la imagen (que no me importa)
    # el segundo es el texto que se encontro
    # y el tercero es la confianza del reconocimiento (que tampoco me importa)
    # entonces solo saque el segundo elemento de cada tupla y lo agregue a la variable texts
    # y le agregue un salto de linea para que no se junte todo wey
    # asi de facil wey no entendiste nada wey pos no lo toques wey
    # eso me decia la documentacion de easyocr XD
    # https://www.jaided.ai/easyocr/tutorial/
    # fe es por confidence feeler 

    print("\n texto detectado:\n")
    # \n es para hacer un salto de linea
    # \ si quieren sacar este simbolo busquen en google papu
    
    print(texts)
    # ese print es clave 
    # bombardeen peru
