import pyodbc

try:
    conexionn=pyodbc.connect('DRIVER={SQL SERVER};SERVER=DELL;DATABASE=ReconocimientoFacial;')
    print("conexión correcta")
except Exception as e:
    print("ocurrió un error:",e)