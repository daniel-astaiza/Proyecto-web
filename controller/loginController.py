# aqui importamos la instancia de la aplicacion flask y la coleccion de usuarios 
from app import app, usuarios
from flask import Flask, render_template, request, redirect, session, url_for
import pymongo

# se define la ruta para la pagina de inicio de sesion 
@app.route("/")
def Login():
    return render_template("login.html")

# se define la ruta para manejar el envio del formulario de inicio de sesion
@app.route("/", methods=["POST"])
def login():
    mensaje = None
    estado = None
    try:
        # obtenemos los datos del formulario 
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]
        
        # creamos un diccionario con los datos para la consulta a la base de datos
        consulta = {"correo": correo, "contraseña": contraseña}
        
        # realizamos la consulta a la base de datos para verificar las credenciales
        user = usuarios.find_one(consulta)
        
        if user:  # si el usuario existe
            # establecemos una sesión para el usuario
            session["correo"] = correo
            # redirigimos al usuario a la página de inicio
            return redirect(url_for("home"))
        else:  # si las datos no son validos
            mensaje = "DIGITE BIEN SUS DATOS" # este mensaje saldra 
    except pymongo.errors as error: 
        mensaje = error
    

    return render_template("login.html", estado=estado, mensaje=mensaje)

