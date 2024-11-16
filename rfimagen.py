import cv2
from deepface import DeepFace
import time
 
imagen_multitud = cv2.imread('imagenes/japan-220696_1280.jpg') 
cara_persona_extraviada=cv2.imread('Galeria/caraprueba.png')

def verificar_cara(imagen_multitud, cara_extraviada):
    resultado = DeepFace.verify(imagen_multitud, cara_extraviada, 
                                model_name="Facenet512", 
                                distance_metric="cosine", 
                                enforce_detection=False,  
                                detector_backend="mtcnn", 
                                threshold=0.4, 
                                normalization="base")
   
    return resultado['verified'], resultado
      
        
  
hay_rostro = False
inicio = time.time() 
try: 
     ver, resultado_verificacion = verificar_cara(imagen_multitud, cara_persona_extraviada)
     if ver:
        datos_cara = resultado_verificacion['facial_areas']['img1']
        x = datos_cara['x']
        y = datos_cara['y']
        w = datos_cara['w']
        h = datos_cara['h']
        cv2.rectangle(imagen_multitud, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(imagen_multitud, 'Coincidencia Encontrada', (x-10, y-10), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Coincidencia', imagen_multitud)
               
     else:
        print("Sin coincidencia")
 
except Exception as e:
            print(f"Error al verificar rostro: {e}")
       
cv2.imshow("Imagen de una multitud", imagen_multitud)
cv2.waitKey(0)
cv2.destroyAllWindows()

