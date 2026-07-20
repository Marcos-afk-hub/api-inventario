from sqlalchemy.orm import Session
import models
import schemas
from auth import hashear_contraseña

#CREATE
def crear_producto(db: Session, producto: schemas.ProductoCrear):
    nuevo_producto = models.Producto(**producto.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

#READ - Todos
def obtener_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

#READ - Solo uno
def obtener_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

#UPDATE
def actualizar_producto(db: Session, producto_id: int, datos: schemas.ProductoActualizar):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        return None
    
    #Solo actualizamos los campos que llegaron
    datos_dict = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_dict.items():
        setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)
    return producto

#DELETE
def eliminar_producto(db: Session, producto_id: int):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        return None
    db.delete(producto)
    db.commit()
    return producto

#Usuarios
def obtener_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def crear_usuario(db: Session, usuario: schemas.UsuarioCrear):
    contraseña_hash = hashear_contraseña(usuario.contraseña)
    nuevo_usuario = models.Usuario(
        email=usuario.email,
        nombre=usuario.nombre,
        contraseña_hash=contraseña_hash
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario