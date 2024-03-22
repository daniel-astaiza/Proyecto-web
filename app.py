from flask import Flask
import pymongo

# aqui se crea una instancia de flask
app = Flask (__name__)

# se configura para la carpeta de imagenes
app.config["UPLOAD_FOLDER"]="./static/imagenes"

# se conecta a la base de datos mongoDB
miConexion = pymongo.MongoClient("mongodb://localhost:27017")

#aqui se selcciona la base de datos y mas abajo estan las colecciones
baseDatos = miConexion["GESTIONPRODUCTOS"]

productos = baseDatos ["PRODUCTOS"]
categoria = baseDatos["CATEGORIAS"]
usuarios = baseDatos ["USUARIOS"]
# aqui es una clave secreta para la aplicacion flask para uso de sesiones
app.secret_key="fff"

from controller.productoController import * 
from controller.loginController import *
if __name__ == "__main__":
    app.run(port=4000, debug=True)
    