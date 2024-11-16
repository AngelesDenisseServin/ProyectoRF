import cv2
from deepface import DeepFace
import time
import os

video = cv2.VideoCapture('videosdepruebas/video3.mp4')
cara_persona_extraviada = cv2.imread('Galeria/Denisse/cara.png') 

carpeta_coincidencias = 'Coincidencias_video3_m'
if not os.path.exists(carpeta_coincidencias):
    os.makedirs(carpeta_coincidencias)
def verificar_cara(Fotograma, cara_extraviada):
    resultado = DeepFace.verify(Fotograma, cara_extraviada, 
                                model_name="Facenet512", 
                                distance_metric="cosine", 
                                enforce_detection=False,  
                                detector_backend="mtcnn", 
                                threshold=0.4, 
                                normalization="base")
   
    return resultado['verified'], resultado
 
if not video.isOpened():
    print("Error al abrir el archivo de video.")
    exit()
 
contador_fotogramas = 0
while True:
    resultado, fotograma = video.read()
    if resultado: 
        contador_fotogramas += 1
        try: 
            ver, resultado_verificacion = verificar_cara(fotograma, 'Galeria/Denisse/carap.png')
            if ver:
                datos_cara = resultado_verificacion['facial_areas']['img1']
                x = datos_cara['x']
                y = datos_cara['y']
                w = datos_cara['w']
                h = datos_cara['h']
                cv2.rectangle(fotograma, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(fotograma, 'Coincidencia Encontrada!', (x-10, y-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Coincidencia', fotograma)
                nombre_imagen = os.path.join(carpeta_coincidencias, f'coincidencia_{contador_fotogramas}.png')
                cv2.imwrite(nombre_imagen, fotograma)
                print(f'Imagen guardada: {nombre_imagen}')
            else:
                print("Sin coincidencia")
 
        except Exception as e:
            print(f"Error al verificar rostro: {e}")
    else:
        print("Error: El fotograma no se leyó correctamente o fin del video.")
        break 
    
    cv2.imshow('Video', fotograma)

video.release()
cv2.destroyAllWindows()
