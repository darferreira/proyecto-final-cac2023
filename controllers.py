from models import *
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from app import app,ma
import time
import os

# Establecer la carpeta pública del servidor que aloja las imágenes de los productos
app.config['FOLDER_IMG_PRODUCTOS'] = 'public/img/productos'
# Establecer la ruta lógica del servidor que aloja las imágenes de los productos
app.config['PATH_IMG_PRODUCTOS'] = 'api/productos/img'

class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','imagen','descripcion')

producto_schema=ProductoSchema()            # El objeto producto_schema es para traer un producto
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto
# crea los endpoint o rutas (json)
@app.route('/api/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()         # el metodo query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla

@app.route('/api/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)   # retorna el JSON de un producto recibido como parametro

@app.route(f"/{app.config['PATH_IMG_PRODUCTOS']}/<filename>",methods=['GET'])
def get_img_producto_by_id(filename):
    return send_from_directory(app.config['FOLDER_IMG_PRODUCTOS'], filename)


@app.route('/api/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    nombre=request.form['nombre']
    precio=request.form['precio']
    stock=request.form['stock']
    foto=request.files['imagen']
    descripcion=request.form['descripcion']

    # Toma el nombre del archivo original como entrada y devuelve un nombre de archivo seguro para su almacenamiento.
    nombre_imagen = secure_filename(foto.filename)
    # Separa el nombre del archivo de su extensión, considerando el punto como separador.
    nombre_extension = os.path.splitext(nombre_imagen)
    # Guarda la imagen con el nombre base y la hora.
    nombre_imagen = f"prod_{int(time.time())}{nombre_extension[1]}"
    foto.save(os.path.join(app.config['FOLDER_IMG_PRODUCTOS'], nombre_imagen))

    #foto.filename = nombre_imagen
    url_foto = f"/{app.config['PATH_IMG_PRODUCTOS']}/{nombre_imagen}"

    new_producto=Producto(nombre,precio,stock,url_foto,descripcion)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)


@app.route('/api/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    # Obtengo el producto a actualizar
    producto=Producto.query.get(id)
    
    # Obtener los datos del form
    nombre=request.form['nombre']
    precio=request.form['precio']
    stock=request.form['stock']
    descripcion=request.form['descripcion']

    # print(request.files['imagen'])
    # Procesar la imagen si no esta vacia
    foto=request.files['imagen']
    
    if foto.filename !='':
        nombre_imagen=secure_filename(foto.filename)
        nombre_extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"prod_{int(time.time())}{nombre_extension[1]}"
        foto.filename = nombre_imagen
        foto.save(os.path.join(app.config['FOLDER_IMG_PRODUCTOS'], nombre_imagen))

        url_foto = f"/{app.config['PATH_IMG_PRODUCTOS']}/{nombre_imagen}"
        producto.imagen=url_foto

    # url_foto = f"/{app.config['PATH_IMG_PRODUCTOS']}/{nombre_imagen}"

    producto.nombre=nombre
    producto.precio=precio
    producto.stock=stock
    
    producto.descripcion=descripcion

    db.session.commit()
    return producto_schema.jsonify(producto)


@app.route('/api/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)   # me devuelve un json con el registro eliminado


@app.route('/api/searchProductos/<string:criterio>', methods=['GET'])
def get_productos(criterio):
    filtered_productos = Producto.query.filter(Producto.nombre.like(f"%{criterio}%")).all()
    result = productos_schema.dump(filtered_productos)
    return jsonify(result)
