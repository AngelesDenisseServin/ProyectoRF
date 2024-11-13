import cv2
from deepface import DeepFace
import time
import os  

video = cv2.VideoCapture('videograbado/video5.mp4')
cara_persona_extraviada = cv2.imread('Galeria/Denisse/cara_t.png')
carpeta_guardado = 'Fotogramas_video5'
if not os.path.exists(carpeta_guardado):
    os.makedirs(carpeta_guardado)
def verificar_cara(cara_recortada, cara_extraviada):
    resultado_cara = DeepFace.verify(cara_recortada, cara_extraviada, 
                                model_name="Facenet512", 
                                distance_metric="cosine", 
                                enforce_detection=False,  
                                detector_backend="mtcnn", 
                                threshold=0.3, 
                                normalization="base")
    return resultado_cara['verified']

contador_fotogramas = 0
procesar_cada_n_fotogramas =20   

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

    if contador_fotogramas % procesar_cada_n_fotogramas == 0:
        try:
            fotograma=cv2.resize(fotograma,(0,0),fx=0.7,fy=0.7)
            caras = cascada_cara.detectMultiScale(fotograma, 1.1, 5, minSize=(24, 24))
            for (x, y, w, h) in caras:
                caradeimagen_recortada = fotograma[y:y+h, x:x+w]  
                hay_cara = verificar_cara(caradeimagen_recortada, cara_persona_extraviada)
               
                if hay_cara:
                    cv2.rectangle(fotograma, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(fotograma, 'Coincidencia Encontrada!', (x-10, y-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.imshow('Coincidencia', fotograma)

                    ruta_guardado = os.path.join(carpeta_guardado, f'fotograma_{contador_fotogramas}.png')
                    cv2.imwrite(ruta_guardado, fotograma)

            else:
                cv2.putText(fotograma, 'Sin Coincidencia', (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                ruta_guardado = os.path.join(carpeta_guardado, f'fotograma_{contador_fotogramas}_1.png')
                cv2.imwrite(ruta_guardado, fotograma)
        except Exception as e:
            print(f"Error al verificar rostro: {e}")

    cv2.imshow('Video', fotograma)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

fin = time.time()
print("Tiempo del programa es:", (fin - inicio) * 10**3, "ms")

video.release()
cv2.destroyAllWindows()
