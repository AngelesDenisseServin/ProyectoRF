import cv2
from deepface import DeepFace
import time
import os  

video = cv2.VideoCapture('videos/video1.mp4')
cara_persona_extraviada = cv2.imread('Galeria/Denisse/cara.png') 
carpeta_guardado = 'Fotogramas_video1_videos'
inicio = time.time()
if not os.path.exists(carpeta_guardado):
    os.makedirs(carpeta_guardado)
def verificar_cara(Fotograma, cara_extraviada):
    resultado = DeepFace.verify(Fotograma, cara_extraviada, 
                                model_name="Facenet512", 
                                distance_metric="cosine", 
                                enforce_detection=False,  
                                detector_backend="mtcnn", 
                                threshold=0.4, 
                                normalization="base")
   
    return resultado['verified'], resultado

contador_fotogramas = 0
#procesar_cada_n_fotogramas =5   

if not video.isOpened():
    print("Error al abrir el archivo de video.")
    exit()


inicio = time.time()
cascada_cara = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while video.isOpened():
    resultado, fotograma = video.read()
    if not resultado or fotograma is None:
        print("Error: El fotograma no se leyó correctamente o fin del video.")
        break  
    
    contador_fotogramas += 1

    #if contador_fotogramas % procesar_cada_n_fotogramas == 0:
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
               # nombre_imagen = os.path.join(carpeta_guardado, f'coincidencia_{contador_fotogramas}.png')
                #cv2.imwrite(nombre_imagen, fotograma)
                #print(f'Imagen guardada: {nombre_imagen}')
            else:
                print("Sin coincidencia")
 
    
            fin = time.time()
            print("Tiempo del programa es:", (fin - inicio) * 10**3, "ms")
            nombre_imagen = os.path.join(carpeta_guardado, f'coincidencia_{contador_fotogramas}.png')
            cv2.imwrite(nombre_imagen, fotograma)
            print(f'Imagen guardada: {nombre_imagen}')
    except Exception as e:
            print(f"Error al verificar rostro: {e}")

    cv2.imshow('Video', fotograma)

fin = time.time()
print("Tiempo del programa es:", (fin - inicio) * 10**3, "ms")

video.release()
cv2.destroyAllWindows()
