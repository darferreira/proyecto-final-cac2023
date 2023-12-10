from datetime import datetime
from app import db,app

# defino la tabla
class Producto(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    precio=db.Column(db.Float)
    stock=db.Column(db.Integer)
    imagen=db.Column(db.String(400))
    descripcion=db.Column(db.String(200))

    def __init__(self,nombre,precio,stock,imagen,description):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.precio=precio
        self.stock=stock
        self.imagen=imagen
        self.descripcion=description


with app.app_context():
    db.create_all()  # aqui crea todas las tablas