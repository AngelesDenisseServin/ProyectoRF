import cv2
from deepface import DeepFace
import os
import time
 
imagen_multitud = cv2.imread('imagenes/japan-220696_1280.jpg') 
cara_persona_extraviada=cv2.imread('Galeria/caraprueba.png')
imagen_multitud = cv2.resize(imagen_multitud,(0,0),fx=0.7,fy=0.7)
#cara_persona_extraviada=cv2.resize(cara_persona_extraviada,(0,0),fx=0.7,fy=0.7)
cascada_cara = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
caras = cascada_cara.detectMultiScale(imagen_multitud, 1.1, 5, minSize=(24, 24))
def verificar_cara(cara_recortada, cara_extraviada): 
    resultado_cara = DeepFace.verify(cara_recortada, cara_extraviada, 
                                model_name="Facenet512", 
                                distance_metric="cosine", 
                                enforce_detection=False,  
                                detector_backend="mtcnn", 
                                threshold=0.3, 
                                normalization="base")
    for r in resultado_cara:
      
         print(r)
    return resultado_cara['verified']
hay_rostro = False
inicio = time.time()
for (x, y, w, h) in caras:
    rostrodeimagen_recortada = imagen_multitud[y:y+h, x:x+w]
    hay_coincidencia = verificar_cara(rostrodeimagen_recortada, cara_persona_extraviada)  
    if hay_coincidencia:   
        hay_rostro = True
        cv2.rectangle(imagen_multitud, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(imagen_multitud, 'Persona Encontrada', (x-10, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        print("coincidencia encontrada")
        
        break;
    else:
        print("No se encontraron coincidencias")
       
cv2.imshow("Imagen de una multitud", imagen_multitud)
cv2.waitKey(0)
cv2.destroyAllWindows()
