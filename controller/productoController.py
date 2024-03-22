# aqui se colocan las importaciones que son necesarias
from app import app, productos, categoria, baseDatos, usuarios
from flask import Flask, render_template, request, jsonify, redirect, url_for,session
import pymongo
import os
from bson.objectid import ObjectId
from io import BytesIO
from bson.json_util import dumps
from pymongo import MongoClient
from controller.loginController import *

# esta es la ruta para la pagina de inicio
@app.route('/home')
def home():
      # se verifica si el usuario ha iniciado sesion exitosamente
    if("correo" in session):
        listaProductos = productos.find()
        todos_productos = []

        for producto in listaProductos:
            cat = categoria.find_one({'_id': ObjectId(producto['categoria'])})
            if cat:
                producto['categoria'] = cat['nombre']
                todos_productos.append(producto)
        return render_template("listarProductos.html", productos=todos_productos)
    else:
        # si no hay sesion iniciada  mandara al usuario a la pagina de inicio de sesion
        mensaje = "ingrese sus campos correctamente"
        return render_template("login.html", mensaje=mensaje)
        
@app.route ("/vistaAgregarProducto")
def vistaAgregarProducto():
     if("correo" in session):
        listaCategorias = categoria.find()
        return render_template("formulario.html",categorias=listaCategorias)
     else:
        mensaje = "ingrese sus campos correctamente"
        return render_template("login.html", mensaje=mensaje)
# esta es la ruta para agregar un producto
@app.route("/vistaAgregarProducto", methods=["POST"])
def agregarProducto():
    # se verifica si el usuario ha iniciado sesion exitosamente
    if("correo" in session):
        mensaje = None
        estado = False
        try:
            # se obtiene los datos del formulario
            codigo =int(request.form["codigo"]) 
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto =request.files["imagen"]
            
            # se crea el campo de producto
            producto ={
                "codigo":codigo,
                "nombre":nombre,
                "precio":precio,
                "categoria":ObjectId(idCategoria)
            }
            
            # aqui se ingresa el producto en la base de datos automaticamente
            resultado = productos.insert_one(producto)
            if (resultado.acknowledged):
                # si todo esta normal se guardara la imagen del producto
                idProducto = resultado.inserted_id
                nombreFoto = f"{idProducto}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreFoto))
                mensaje = "producto Agregado Correctamente"
                estado = True
                return redirect (url_for("home"))
            else:
                mensaje="problemas al agregar"

            return render_template ("/formulario.html",estado= estado, mensaje=mensaje,)


        except pymongo.errors as error:
            mensaje = error
            return error
    else:
        mensaje = "ingrese sus campos correctamente"
        return render_template("login.html", mensaje=mensaje)
    
    
@app.route("/salir")
def salir():
    session.clear()
    mensaje="se ha cerrado sesion correctamente"
    return render_template("login.html",mensaje=mensaje)
    
@app.route("/eliminar_producto/<producto_id>", methods=["POST"])
def eliminar_producto(producto_id):
    # Verifica si el usuario ha iniciado sesión
    if "correo" in session:
        try:
            # Convierte el ID del producto a un objeto ObjectId
            producto_obj_id = ObjectId(producto_id)
            # Elimina el producto de la base de datos
            productos.delete_one({"_id": producto_obj_id})
            # Redirige a la página de inicio
            return redirect(url_for("home"))
        except pymongo.errors.PyMongoError as error:
            # Maneja errores de MongoDB
            return render_template("error.html", mensaje="Error al eliminar el producto")
    else:
        # Si el usuario no ha iniciado sesión, redirige a la página de inicio de sesión
        mensaje = "Por favor inicia sesión para continuar."
        return render_template("login.html", mensaje=mensaje) 
    


@app.route("/actualizarProducto/<producto_id>", methods=["POST"])
def actualizar_producto(producto_id):
    if "correo" in session:
        try:
            codigo = int(request.form["codigo"]) 
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto = request.files["imagen"]

            producto_actualizado = {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": ObjectId(idCategoria)
            }

            productos.update_one({"_id": ObjectId(producto_id)}, {"$set": producto_actualizado})

            if foto:
                nombreFoto = f"{producto_id}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))

            return redirect(url_for("home"))

        except pymongo.errors.PyMongoError as error:
            return f"Error al actualizar el producto: {error}"
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)
    
    
@app.route("/editar_producto/<producto_id>", methods=["GET"])
def editar_producto(producto_id):
    if "correo" in session:
        try:
            producto = productos.find_one({"_id": ObjectId(producto_id)})
            if producto:
                listaCategorias = categoria.find()
                return render_template("EditarProducto.html", producto=producto, categorias=listaCategorias)
            else:
                return "Producto no encontrado."
        except pymongo.errors.PyMongoError as error:
            return f"Error al cargar el producto: {error}"
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)
    
    

            
    

    
    



