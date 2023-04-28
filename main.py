import fitz
#Librería para Realizar Resumen 
import bs4 as bs  
import urllib.request  
import re
import nltk
import bs4
import urllib.request
import requests
from bs4 import BeautifulSoup
import urllib.request
from inscriptis import get_text
from googletrans import Translator #Para la version de googletrans ==3.1.0a0 
from pdfminer.high_level import extract_text
from nltk import word_tokenize,sent_tokenize
import heapq  
nltk.download('punkt')
nltk.download('stopwords')
#Librería para leer txt utf-8
import codecs

def PdfToHTML():
    #Insertamos el PDF
    pdf = "/content/CV.pdf" 
    documento = fitz.open(pdf)
    pagina = documento.load_page(0)
    doc = fitz.open(pdf)
    salida = open(pdf+".html","wb")
    for pagina in doc:
        texto = pagina.get_text("html").encode("utf8")
        salida.write(texto)
        salida.write(b"\n--------------------\n")
    salida.close()
    Resumen()   

def Resumen():
    #Insertamos el PDF
    pdfTohtml = extract_text("/content/CV.pdf")
    articulo_texto = pdfTohtml
    articulo_texto = articulo_texto.replace("[ edit ]", "")
    print ("Resumen del texto")
    print ("------------------")


    # Elimina palabras vacías, espacios extras
    articulo_texto = re.sub(r'\[[0-9]*\]', ' ', articulo_texto)  
    articulo_texto = re.sub(r'\s+', ' ', articulo_texto)  

    formatear_articulo = re.sub('[^a-zA-Z]', ' ', articulo_texto )  
    formatear_articulo = re.sub(r'\s+', ' ', formatear_articulo)  
    
    lista_palabras = nltk.sent_tokenize(articulo_texto)  
    stopwords = nltk.corpus.stopwords.words('english')

    frecuencia_palabras = {}  
    for word in nltk.word_tokenize(formatear_articulo):  
        if word not in stopwords:
            if word not in frecuencia_palabras.keys():
                frecuencia_palabras[word] = 1
            else:
                frecuencia_palabras[word] += 1
    max_frecuencia = max(frecuencia_palabras.values())

    for word in frecuencia_palabras.keys():  
        frecuencia_palabras[word] = (frecuencia_palabras[word]/max_frecuencia)

    #Calcula frases repetidas
    rep_oraci = {}  
    for sent in lista_palabras:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in frecuencia_palabras.keys():
                if len(sent.split(' ')) < 500: # -----------> El numero cambia segun el numero de paginas, y cuan largo queremos que sea el resumen
                    if sent not in rep_oraci.keys():
                        rep_oraci[sent] = frecuencia_palabras[word]
                    else:
                        rep_oraci[sent] += frecuencia_palabras[word]
    
    #Resumen
    resumen_oracion = heapq.nlargest(7, rep_oraci, key=rep_oraci.get)
    resumen = ' '.join(resumen_oracion)  
    print(resumen) # -----------> Imprime el resuen del texto en la termianl en el idioma original
    
    #Traducción
    translator = Translator()
    translate = translator.translate(resumen, src="en", dest="ja") # -----------> src=idioma original - dest= idioma al que queremos traducir

    #Guardar en .txt
    resumenpdf = open("Resumen.txt","w")
    resumenpdf.write("Resumen del texto:\n" + translate.text)
    resumenpdf.close() # -----------> El texto guardado en el .txt estara en el lenguaje que definamos en #Traducción
    
PdfToHTML()