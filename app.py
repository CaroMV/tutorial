import os #<- os nos permite tener acceso a las paths / direcciones de nuestro compu/ crear carpretas / crear nuevas rutas

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from models.imagen import Imagen

app = Flask(__name__)


UPLOAD_FOLDER = "static/uploads" #<--- Creamos una variable que contiene el inicio del directorio que vamos a usar para guardar las imagenes


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #<---- como nuestros proyectos son modularizados, es útil tener asignado como configuración general que la carpeta para guardar estos archivos esté asignada en la instancia app, como parte de su configuración
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} #<--- ¿Qué tipo de extensiones vamos a permitir? 

#Creamos una función o podríamos incluso hacer un método para validar la imagen, utilizando una forma de expresión regular
#En este caso, "nombre del archivo" "." y que termine con una de las extensiones permitidas

def extension_permitida(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    imagenes = Imagen.obtener_todas()
    return render_template("listado.html", imagenes=imagenes)


@app.route('/subir')
def subir():
    return render_template("subir.html")


@app.route('/guardar', methods=['POST'])
def guardar():

    #acá cree pequeñas validaciones similares a las que hacemos en proyectos
    #Si no se encuentra un "archivo" entre los request.files, entonces no envió el archivo
    if 'archivo' not in request.files:
        return "No enviaste archivo"

    #Si lo envió, entonces, lo guardo en una variable
    archivo = request.files['archivo']

    #Si el nombre del archivo no tiene nombre es algo que no tenemos permitido
    if archivo.filename == '':
        return "Archivo vacío"

    #Si pasa las validaciones que hicimos
    if archivo and extension_permitida(archivo.filename):

        #secure_filename normaliza el nombre del archivo para que sea seguro en el filesystem, permitiendo no tener caracteres extraños
        nombre_seguro = secure_filename(archivo.filename)

        #acá vamos a construir la ruta del archivo a guardar: 
                    #usando OS.crea un path. que viene de la unión(la carpeta de upload/nombre_seguro)
        ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro)

        #guarda el archivo en la ruta que creamos arriba
        #! NO CONFUNDIR CON EL METODO SAVE DE UNA CLASE, ESTE SAVE GUARDA EN NUESTRAS DEPENDENCIAS
        archivo.save(ruta_completa)


        #! Ahora si vamos a usar la clase:

        data = {
            "titulo": request.form['titulo'],
            "ruta": ruta_completa  #* solo guardamos la ruta
        }
        #Guardamos los datos en nuestra base de datos de imagenes, el titulo y la ruta del archivo que está en nuestro disco
        Imagen.guardar(data)

        return redirect('/')

    return "Formato no permitido"
    

if __name__ == "__main__":
    app.run(debug=True)
