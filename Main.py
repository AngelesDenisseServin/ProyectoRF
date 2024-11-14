from fasthtml.common import *
from fasthtml.components import Some_never_before_used_tag
from conexion import conexionn
from deepface import DeepFace
import shutil
from fastapi.responses import StreamingResponse
from fastcore.parallel import threaded
from starlette.datastructures import UploadFile
from flask import  request, redirect, url_for
from fastapi.responses import RedirectResponse
from PIL import Image
import cv2
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import glob



scrips=(Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),Script(src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js",integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" ,crossorigin="anonymous"),Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js", integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy", crossorigin="anonymous"))
gridlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css")


app,rt = fast_app(hdrs=(scrips,gridlink))
mensaje=0
hay_coincidenciapagina=0
mensaje_registro_usuario=0
rutaimg=""
banderabuscar=0
video_ruta='videosdepruebas/video1.mp4'
bandera=0
Nombre_persona_registradaimg=''
id_historial=0


@app.route('/')
def get():
    if os.path.isfile('Galeriap/imagen_cargada.png'):
        os.remove('Galeriap/imagen_cargada.png')
        print("Archivo eliminado correctamente.")
    else:
        print("Imagen cargada borrada")
    if os.path.isdir('Coincidencias_web'): 
        for archivo in glob.glob(os.path.join('Coincidencias_web', '*')): 
            if os.path.isfile(archivo):  
                os.remove(archivo)  
                print(f"Archivo {archivo} eliminado.")
        print("Carpeta vacía.")
    
    cv2.destroyAllWindows()
    global mensaje
    usuariot = Input( name="usuarion",style=" color:black;display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);",method="post")
    contraset = Input( name="contrasen",type="password",style=" color:black;display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);",  hx_swap_oob='true',method="post")
    alerta=Div(P("Datos invalidos. Por favor intente de nuevo",style="color:red;"))
    inicio=Button("Iniciar sesión", method="post",type="submit",style="border-radius: 25px;")
    registro=Button("Registrar", method="post",type="submit",style="border-radius: 25px;background-color: #008080;")
    Formulario = Main(cls="mb-3",style="display: flex;justify-content: center;align-items: center;height: 100vh;margin: 0;background-color: #f0f0f0;")(
         Div(style="align-items: center;background: linear-gradient(to bottom, #d3d3d3, #a9a9a9);padding: 50px 30px;border-radius: 12px;width: 350px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")(
                        Form(action="/p/",style="")(
           Div(Label('Usuario',style="color:black;")),
           Div(usuariot),
           Div(Label("Contraseña",style="color:black;")),
           Div(contraset),
           Form(action="/p/",style="")(inicio),
           Form(action="/regis")(registro)
                )))
    Formularioalerta = Main(cls="mb-3",style="display: flex;justify-content: center;align-items: center;height: 100vh;margin: 0;background-color: #f0f0f0;")(
         Div(style="align-items: center;background: linear-gradient(to bottom, #d3d3d3, #a9a9a9);padding: 50px 30px;border-radius: 12px;width: 350px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")(
                        Form(action="/p/",style="")(
        
           Div( Label('Usuario',style="color:black;")),
           Div(usuariot),
           Div( Label("Contraseña",style="color:black;")),
           Div(contraset),
           alerta,
           Form(action="/p/",style="")(inicio),
           Form(action="/regis")(registro)     
                )))

    if mensaje==0:
      return Formulario
    else: 
         mensaje=0 
         return Formularioalerta

@rt('/p/')
def get(usuarion:str,contrasen:str):
     global mensaje
     with conexionn.cursor() as cursor:
        cursor.execute("USE ReconocimientoFacial")
        consulta = "SELECT * FROM UsuariosRF WHERE Usuario=? AND Contraseña=?"
        cursor.execute(consulta,(usuarion, contrasen))
        resultado=cursor.fetchall() 
        print(resultado)
        if resultado:         
                return RedirectResponse(url="/paginaprincipal")
        else:
                mensaje=1
                return RedirectResponse(url="/")

@app.route('/paginaprincipal')
def get():  
    img_ruta ="Galeriap/imagen_cargada.png"
    if not os.path.exists(img_ruta):
        img_ruta = "https://cdn-icons-png.flaticon.com/512/144/144808.png"
    
    pagina= Main(style="height: 100%;padding:0;")(Title("Pagina principal"),
            Nav(cls="navbar navbar-light bg-light")(Form(cls="container-fluid",style="padding:1em;")(Button("Regresar",style="background:#00C7BE;color:white;width:150px;",cls="btn btn-primary btn-lg"),A(" ",cls="navbar-brand"),Button("Salir",style="background:red;width:150px;",cls="btn btn-primary btn-lg"),action="/")),
            Div(cls="form",style="padding: 1px 30px;height:50%;")( 
            Group(cls="center-xs",style="padding:0;")(
            Card(cls="card",style="width:20%;")(
                 Img(style="width:200px;height:120px;", src=img_ruta),
                    Div(cls="card-body")(P("Botones",style="visibility: hidden;"),Form(action='/buscarpersona')(Button("Buscar",style="padding: 1em;border-radius: 5px;",type="submit")),
                        Form(action="/cargar-imagen" , method="post")(                                                                     
                        Input(name="imagen", type="file"), Button("Cargar Imagen",style="padding: 1em; border-radius: 5px;",type="submit")),
                        Form(action="/registroimg")(Button("Registrar persona extraviada",style="padding: 1em;border-radius: 5px;",type="submit")),
                        Form(action="/Guardar")(Button("Guardar coincidencias encontradas",style="padding: 1em;border-radius: 5px;",type="submit")),
                        Form(action="/buscar")(Button(style="padding: 1em;border-radius: 5px;")("Historial de busquedas",type="submit"))
                        )),
            Figure(cls="figure",style="width:80%;")(
                 Img(cls="figure-img img-fluid rounded",style="width:1050px;height:580px;",src="/video_feed")
                 ))
            ,
            Div(cls="mb-3 center-xs")(Button(style="width:95%;align-items: center;background-color: #00b894;")("Cambiar cámara",type="submit")),
            cls="go" ))
    
    
    return pagina

def generar_frames(): 
    global video_ruta 
    cam = cv2.VideoCapture(video_ruta)
    if not cam.isOpened():
        return "Error al abrir la cámara"
   
    while True:
        ret, fotograma = cam.read()
        if not ret:
            break   
        ret, buffer = cv2.imencode('.jpg', fotograma)
        if not ret:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def generar_framesbuscar():
    bandera_coincidencia=0
    cara_persona_extraviada = cv2.imread('Galeria/Denisse/cara_t3.png')
    carpeta_coincidencias = 'Coincidencias_web'
    if not os.path.exists(carpeta_coincidencias):
        os.makedirs(carpeta_coincidencias)
    global video_ruta  
    cam = cv2.VideoCapture(video_ruta)
    if not cam.isOpened():
        return "Error al abrir el video"
    contador_fotogramas = 0
    procesar_fotogramas = 5 
    while True:
        ret, fotograma = cam.read()
        if not ret or fotograma is None:
            print("Error: El fotograma no se leyó correctamente o fin del video.")
            break 
        if os.path.isfile('Galeriap/imagen_cargada.png'):
            contador_fotogramas += 1
            if contador_fotogramas % procesar_fotogramas == 0:
                try:
                    cascada_cara = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                    caras = cascada_cara.detectMultiScale(fotograma, 1.1, 5, minSize=(24, 24))
                    cara_persona_extraviada=cv2.imread('Galeriap/imagen_cargada.png')
                    
                    for (x, y, w, h) in caras:
                        caradeimagen_recortada = fotograma[y:y+h, x:x+w] 
                        verificar_cara = DeepFace.verify(caradeimagen_recortada, cara_persona_extraviada, 
                                                            model_name="Facenet512", 
                                                            distance_metric="cosine", 
                                                            enforce_detection=False,  
                                                            detector_backend="mtcnn", 
                                                            threshold=0.3, 
                                                            normalization="base")
                            
                            
                        if verificar_cara['verified']:
                                    bandera_coincidencia=1
                                    cv2.rectangle(fotograma, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                    cv2.putText(fotograma, 'Coincidencia Encontrada!', (x-10, y-10), 
                                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)                                 
                                    print("coincidencia encontrada")
                                    nombre_imagen = os.path.join(carpeta_coincidencias, f'coincidencia_{contador_fotogramas}.png')
                                    cv2.imwrite(nombre_imagen, fotograma)
                                    print(f'Imagen guardada: {nombre_imagen}')
                                        
                        else:
                                
                                     print("Sin coincidencia")
                except Exception as e:
                         print(f"Error al verificar rostro: {e}")
        if bandera_coincidencia==1:
                cv2.putText(fotograma, 'Coincidencia Encontrada!', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', fotograma)
        if not ret:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cam.release()

@app.route('/video_feed')
def video_feed():
    global banderabuscar
    if banderabuscar==1:
        return StreamingResponse(generar_framesbuscar(), media_type='multipart/x-mixed-replace; boundary=frame')
    else:
        return StreamingResponse(generar_frames(), media_type='multipart/x-mixed-replace; boundary=frame')
    
@app.post("/cargar-imagen")
def cargar_imagen(imagen: UploadFile ):
    global bandera_ya_registradaimg
    bandera_ya_registradaimg=0
    img_dir = "Galeriap"
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    try:
        img = Image.open(imagen.file)
        global rutaimg
        rutaimg=imagen.file
        img.thumbnail((200, 120))
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        
    img_ruta = os.path.join(img_dir, "imagen_cargada.png")
    img.save(img_ruta)
    print(f"Imagen guardada en: {img_ruta}")
    rutaimg=img_ruta
    return RedirectResponse(url="/paginaprincipal", status_code=302)
  
@app.route('/regis')
def reintento():
     global mensaje_registro_usuario
     Nombrei=Input(id="Nombre",hx_swap_oob='true',method="post", style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);",name="nombre")
     FechaNacimiento=Input(id="Fecha", name="fecha",type="date",method="post",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     LugarNacimiento=Input(id="Lugar", name="lugar",hx_swap_oob='true',method="post",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     Curp=Input(id="Curp", name="curp",hx_swap_oob='true',method="post",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     Correo=Input(id="Correo", name="correo",hx_swap_oob='true',method="post",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     Telefono=Input(id="Telefono",name="telefono",type="tel",hx_swap_oob='true',method="post",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);" )
     Usuarioi=Input(id="Usuario",name="usuario",method="post",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     Contraseñai=Input(id="Contrasee", name="contrase",type="password",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     alerta=Div(style="color:red;")(P("Datos incompletos. Por favor intente de nuevo",style="color:red;"))
     registro=Button("Registrar",type="submit",style="border-radius: 25px;", name="data")
     Formulario = Form(action="/")(Nav(cls="navbar navbar-light bg-light",style="padding:1em;")(Label('Registro de nuevo usuario'),Button("Regresar",style="background:#CFFFE5;color:black;"))),Main(cls="mb-3",style="display: flex;justify-content: center;align-items: center;margin: 0;background-color: #f0f0f0;")(
         Div(style="display:inline;align-items: center;background: linear-gradient(to bottom, #d3d3d3, #a9a9a9);padding:  30px;border-radius: 12px;width: 450px;")(
                        Form(action="/registrar/",style="display:inline;")(
           
           Div(Label('Nombre completo')),
           Div(Nombrei),
           Div(Label('Fecha de Nacimiento')),
           Div(FechaNacimiento),
           Div(Label('Lugar de Nacimiento')),
           Div(LugarNacimiento),
           Div(Label('CURP')),
           Div(Curp),
           Div( Label('Correo')),
           Div(Correo),
           Div( Label('Teléfono')),
           Div(Telefono),
           Div( Label('Usuario')),
           Div(Usuarioi),
           Div( Label("Contraseña")),
           Div(Contraseñai),
           Div(Label(' ')),
           Div(registro) 
                )))
     Formularioalerta = Form(action="/")(Nav(cls="navbar navbar-light bg-light",style="padding:1em;")(Label('Registro de nuevo usuario'),Button("Regresar",style="background:#CFFFE5;color:black;"))),Main(cls="mb-3",style="display: flex;justify-content: center;align-items: center;margin: 0;background-color: #f0f0f0;")(
         Div(style="display:inline;align-items: center;background: linear-gradient(to bottom, #d3d3d3, #a9a9a9);padding:  30px;border-radius: 12px;width: 450px;")(
                        Form(action="/registrar/",style="display:inline;")(
           alerta,
           Div(Label('Nombre completo')),
           Div(Nombrei),
           Div(Label('Fecha de Nacimiento')),
           Div(FechaNacimiento),
           Div(Label('Lugar de Nacimiento')),
           Div(LugarNacimiento),
           Div(Label('CURP')),
           Div(Curp),
           Div( Label('Correo')),
           Div(Correo),
           Div( Label('Teléfono')),
           Div(Telefono),
           Div( Label('Usuario')),
           Div(Usuarioi),
           Div( Label("Contraseña")),
           Div(Contraseñai),
           Div(Label(' ')),
           Div(registro) 
                )))
     if mensaje_registro_usuario==0:
        return Formulario
     else:
         mensaje_registro_usuario=0
         return Formularioalerta
         
@rt('/registrar/')
def get(nombre:str,usuario:str,contrase:str,correo:str,fecha:date,lugar:str,curp:str,telefono:str):
     global mensaje_registro_usuario
     with conexionn.cursor() as cursorr:
         cursorr.execute("USE ReconocimientoFacial")
         consulta="insert into UsuariosRF values(?,?,?,?,?,?,?,?)"
         cursorr.execute(consulta,(nombre),(correo),(usuario),(contrase),(fecha),(lugar),(curp),(telefono) )     
         cursorr.commit()
         
         consulta = "SELECT * FROM UsuariosRF WHERE Usuario=? AND Contraseña=?"
         cursorr.execute(consulta, (usuario, contrase))
         resultar=cursorr.fetchall()
         if resultar:
              return RedirectResponse(url="/")
         else:
              mensaje_registro_usuario=1
              return RedirectResponse(url="/regis")
@app.route('/registroimg')
def reintento():
     global bandera
     
     Nombrei=Input(id="Nombre", style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);",name="nombre")
     Edad=Input(id="Edad",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);", name="edad")
     Numcontac=Input(id="Numcon", name="Numcont", style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     Nomcontac=Input(id="Nomcont", name="Nomcont", type="datetime",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     Fechadesaparicion=Input(id="FechaD", name="FechaD", type="date",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     Hora=Input(id="Hora", name="hora",style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     Reportante=Input(id="reportante", name="Reportante", style=" display: block;width: 100%;padding: 10px;margin: 10px 0;border: none;border-radius: 25px;background-color: white;box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);")
     alerta=Div(style="color:red;")(P("Datos incompletos. Por favor intente de nuevo",style="color:red;"))
     registro=Form(Button("Registrar",type="submit",style="border-radius: 25px;", name="data"),action="/registrar", method="post")
     Formulario = Nav(cls="navbar navbar-light bg-light",style="padding:.3em;")(Label('Registro de información del indivio en la imagen'),Form(action="/paginaprincipal")(Button("Regresar",style="background:#CFFFE5;color:black;"))),Main(cls="mb-3",style="display: flex;justify-content: center;align-items: center;margin: 0;background-color: #f0f0f0;")(
         Div(style="align-items: center;background: linear-gradient(to bottom, #d3d3d3, #a9a9a9);padding:  30px;border-radius: 12px;width: 350px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")(
                        Form(action="/registrarimg/",style="")(
           Div(Label('Nombre')),
           Div(Nombrei),
           Div( Label('Edad')),
           Div(Edad),
           Div( Label('Fecha de desaparición')),    
           Div(Fechadesaparicion),
           Div( Label('Hora de desaparición')),    
           Div(Hora),
           Div( Label('Reportante')),
           Div(Reportante),
           Div( Label("Nombre de contacto familiar")),
           Div(Nomcontac),   
           Div( Label("Número de contacto")),
           Div(Numcontac),
           Div(Label(' ')),
           Form(action="/regis")(registro)      
                )))
     Formularioalerta = Nav(cls="navbar navbar-light bg-light",style="padding:.3em;")(Label('Registro de información del indivio en la imagen'),Form(action="/paginaprincipal")(Button("Regresar",style="background:#CFFFE5;color:black;"))),Main(cls="mb-3",style="display: flex;justify-content: center;align-items: center;margin: 0;background-color: #f0f0f0;")(
         Div(style="align-items: center;background: linear-gradient(to bottom, #d3d3d3, #a9a9a9);padding:  30px;border-radius: 12px;width: 350px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);")(
                        Form(action="/registrarimg/",style="")(
           alerta,
           Div(Label('Nombre')),
           Div(Nombrei),
           Div( Label('Edad')),
           Div( Label('Fecha de desaparición')),
           Div(Fechadesaparicion),
           Div( Label('Hora de desaparición')),    
           Div(Hora),
           Div( Label('Reportante')),
           Div(Reportante),
           Div( Label("Nombre de contacto familiar")),
           Div(Nomcontac),   
           Div( Label("Número de contacto")),
           Div(Numcontac),
           Div(Label(' ')),
           Form(action="/regis")(registro)    
           
                )))
     if bandera==0:
        return Formulario
     else:
        return Formularioalerta

@rt('/registrarimg/')
def get(nombre:str,edad:str,Numcont:str,Nomcont:str,FechaD:date,hora:str,Reportante:str,):
    global bandera
    global rutaimg
    global Nombre_persona_registradaimg
    carpeta_base = 'Coincidencia'
    carpeta_persona_extraviada = os.path.join(carpeta_base, nombre)
    if not os.path.exists(carpeta_base):
        os.makedirs(carpeta_base)
        print(f"Se creó la carpeta base: '{carpeta_base}'")
    if not os.path.exists(carpeta_persona_extraviada):
        os.makedirs(carpeta_persona_extraviada)
        print(f"Se creó la carpeta: '{carpeta_persona_extraviada}'")
    with conexionn.cursor() as cursorr:
         cursorr.execute("USE ReconocimientoFacial")
         consulta="insert into Datos_de_persona_extraviada values(?,?,?,?,?)"
         cursorr.execute(consulta,(nombre),(rutaimg),(edad),(Nomcont),(Numcont))     
         cursorr.commit()
         consulta = "select Id from Datos_de_persona_extraviada where Nombre=?"
         cursorr.execute(consulta, (nombre))
         resultar=cursorr.fetchall()
         global banderabuscar
         if resultar:
              IdH=''
              for r in resultar:
                            IdH=r[0]
              if banderabuscar==1:
                ruta_completa=''
                extensiones_imagenes = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")
                origen='Coincidencias_web'
                destino=carpeta_persona_extraviada 
                for archivo in os.listdir(origen):
                    ruta_archivo_origen = os.path.join(origen, archivo)
                    ruta_archivo_destino = os.path.join(destino, archivo)
                    if os.path.isfile(ruta_archivo_origen) and archivo.lower().endswith(extensiones_imagenes):
                        shutil.copy2(ruta_archivo_origen, ruta_archivo_destino)
                    print(f"Todas las imágenes se han copiado de '{origen}' a '{destino}'.")
                for archivo in os.listdir(carpeta_persona_extraviada):
                        if archivo.startswith("coincidencia_") and archivo.endswith(".png"):
                                ruta_completa = os.path.join(origen, archivo)
                                fecha_hora_actual = datetime.now()
                                fecha_hora_sql = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
                                cursorr.execute("USE ReconocimientoFacial")
                                consulta="insert into Historial values(?,?,?,?,?,?)"
                                cursorr.execute(consulta,(IdH),(FechaD),(hora),(Reportante),(fecha_hora_sql),(ruta_completa))     
                                cursorr.commit()
                                Nombre_persona_registradaimg=nombre
              else:
                    fecha_hora_actual = datetime.now()
                    fecha_hora_sql = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
                    Nombre_persona_registradaimg=nombre
                    cursorr.execute("USE ReconocimientoFacial")
                    consulta="insert into Historial values(?,?,?,?,?,?)"
                    cursorr.execute(consulta,(IdH),(FechaD),(hora),(Reportante),(fecha_hora_sql),(ruta_completa))     
                    cursorr.commit()                 
              return RedirectResponse(url="/paginaprincipal")
         else:
              bandera=1
              return RedirectResponse(url="/registroimg")

@app.route('/buscarpersona')
def get():
     global banderabuscar
     if os.path.isfile('Galeriap/imagen_cargada.png'):
          banderabuscar=1    
     return RedirectResponse(url="/paginaprincipal")
        
@app.route('/Guardar')
def get():
     global banderabuscar
     banderabuscar=0
     global bandera_ya_registradaimg
     if Nombre_persona_registradaimg!='':
               with conexionn.cursor() as cursorr:
                consulta = "select Id from Datos_de_persona_extraviada where Nombre=?"
                cursorr.execute(consulta, (Nombre_persona_registradaimg))
                resultar=cursorr.fetchall()
                if resultar:
                    ruta_completa=''
                    IdH=''
                    for r in resultar:
                                    IdH=r[0]
                    extensiones_imagenes = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")

                    origen='Coincidencias_web'
                    destino='Coincidencia/'+Nombre_persona_registradaimg
                    for archivo in os.listdir(origen):
                            ruta_archivo_origen = os.path.join(origen, archivo)
                            ruta_archivo_destino = os.path.join(destino, archivo)
                            if os.path.isfile(ruta_archivo_origen) and archivo.lower().endswith(extensiones_imagenes):
                                shutil.copy2(ruta_archivo_origen, ruta_archivo_destino)

                            print(f"Todas las imágenes se han copiado de '{origen}' a '{destino}'.")
                    for archivo in os.listdir(destino):
                                if archivo.startswith("coincidencia_") and archivo.endswith(".png"):
                                        ruta_completa = os.path.join(destino, archivo)
                                        cursorr.execute("USE ReconocimientoFacial")
                                        consulta="select * from Historial where Id=?"
                                        cursorr.execute(consulta,(IdH))     
                                        resultado=cursorr.fetchall()
                                        fecha_hora_actual = datetime.now()
                                        fecha_hora_sql = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
                                        for re in resultado:
                                            
                                            cursorr.execute("USE ReconocimientoFacial")
                                            consulta="insert into Historial values(?,?,?,?,?,?)"
                                            cursorr.execute(consulta,(IdH),(re[1]),(re[2]),(re[3]),(fecha_hora_sql),(ruta_completa))     
                                            cursorr.commit()
                                consultab="DELETE FROM Historial WHERE Resultado_de_busqueda='';"
                                cursorr.execute(consultab)
                                cursorr.commit()
     return RedirectResponse(url="/paginaprincipal")                                      
@app.route('/buscar')
def buscar():
    return Div(style="Padding:1em;")(
          Nav(cls="navbar navbar-light bg-light")(Form(cls="nav-item",action="/paginaprincipal")(Button("Regresar",style="background:#00C7BE;color:white;width:150px;",cls="btn btn-primary btn-lg")),Form(action="/",cls="nav-item")(Button("Salir",style="background:red;width:150px;",cls="btn btn-primary btn-lg"))),
               Div(style="padding:2em;background:#C0C0C0;")(Nav(cls="navbar navbar-light bg-light")(Div(cls="container-fluid")(Form(action="/buscarbd",cls="d-flex")
                (Group(cls="")(Input(cls="form-control me-2",name="parametro", type="search" ),
                Button("Buscar",cls="btn btn-outline-primary", type="submit"))))))
                )

@app.route('/buscarbd')
def buscarbd(parametro:str):
        alerta = Div(style="color:red;")(P("Datos no encontrados", style="color:red;"))
        tabla = ""
        consulta = "SELECT Id,Nombre,Edad,Nombre_Contacto_Familiar,Numero_Contacto_Familiar FROM Datos_de_persona_extraviada WHERE Id LIKE '%" + parametro + "%' OR Nombre LIKE '%" + parametro + "%' OR Edad LIKE '%" + parametro + "%' OR Nombre_Contacto_Familiar LIKE '%" + parametro + "%' OR Numero_Contacto_Familiar LIKE '%" + parametro + "%'; "
        with conexionn.cursor() as cursor:
            cursor.execute(consulta)  
            resultado = cursor.fetchall()
        if resultado:
            tabla = Table(
                Tr(Th("ID"), Th("Nombre"), Th("Edad"), Th("Nombre Contacto"), Th("Número Contacto"),Th(" ")),
                *[Tr(Td(row[0]), Td(row[1]), Td(row[2]), Td(row[3]), Td(row[4]), Td(Form(action="/mostrar_Historial")(Input(type="hidden", name="idbuscar", value=row[0]),Button("Seleccionar",type="submit")))) for row in resultado]
            )
        else:
            tabla = alerta
       
        buscar= Div(Nav(cls="navbar navbar-light bg-light")(Form(cls="nav-item",action="/buscar")(Button("Regresar",style="background:#00C7BE;color:white;width:150px;",cls="btn btn-primary btn-lg")),Form(action="/",cls="nav-item")(Button("Salir",style="background:red;width:150px;",cls="btn btn-primary btn-lg"))),
               Div(style="padding:2em;background:#C0C0C0;")(Nav(cls="navbar navbar-light bg-light")(Div(cls="container-fluid")(Form(action="/buscarbd",cls="d-flex")
                                                                               (Group(cls="")(Input(cls="form-control me-2",name="parametro", type="search" ),
                                                                                Button("Buscar",cls="btn btn-outline-primary", type="submit"))))))
        )
        return Main(style="Padding:1em;")(
            buscar,
            Div(style="padding:2em;background:#C0C0C0;")(
                Nav(cls="navbar navbar-light bg-light")(
                    Div(cls="container-fluid")(
                        Form(action="/mostrar_Historial",cls="d-flex")(tabla)  
                    )
                )
            )
        )
@app.route('/mostrar_Historial')
def mostrarh(idbuscar:int):
     alerta = Div(style="color:red;")(P("No localizada", style="color:red;"))
     with conexionn.cursor() as cursorr:
        consulta="select * from Historial where id=?"
        cursorr.execute(consulta,(idbuscar))
        resultar=cursorr.fetchall()
        if resultar:
            tabla = Table(
                Tr(Th("ID"), Th("Fecha de extravio"), Th("Hora"), Th("Reportante"), Th("Fecha de encuentro de coincidencia "),Th(" ")),
                *[Tr(Td(row[0]), Td(row[1]), Td(row[2]), Td(row[3]), Td(row[4]), Td(Form(action="/ver_coincidencia")(Input(type="hidden", name="rutaver", value=row[5]),Button("Ver",type="submit")))) for row in resultar]
            )
             
        else:
            tabla = alerta

     buscar=Div(Nav(cls="navbar navbar-light bg-light")(Form(cls="nav-item",action="/buscar")(Button("Regresar",style="background:#00C7BE;color:white;width:150px;",cls="btn btn-primary btn-lg")),Form(action="/",cls="nav-item")(Button("Salir",style="background:red;width:150px;",cls="btn btn-primary btn-lg"))),
        )
                                                                                
     return Main(style="Padding:1em;")(
            buscar,
            Div(style="padding:2em;background:#C0C0C0;")(
                Nav(cls="navbar navbar-light bg-light")(
                    Div(cls="container-fluid")(
                        Form(action="/ver_coincidencia",cls="d-flex")(tabla)  
                    )
                )
            )
        )
@app.route('/ver_coincidencia')
def ver(rutaver:str):
     buscar=Div(Nav(cls="navbar navbar-light bg-light")(Form(cls="nav-item",action="/buscar")(Button("Regresar",style="background:#00C7BE;color:white;width:150px;",cls="btn btn-primary btn-lg")),Form(action="/",cls="nav-item")(Button("Salir",style="background:red;width:150px;",cls="btn btn-primary btn-lg"))),
        )
     ruta=rutaver                                                                     
     return Main(style="Padding:1em;")(
            buscar,
            Div(style="padding:2em;display:flex;justify-content:center;align-items:center;height:100vh;")(
             Nav(cls="navbar navbar-light bg-light")(
                 Img(src=ruta, style="max-width:100%;max-height:100%;")
             )
         )
     )
serve()
