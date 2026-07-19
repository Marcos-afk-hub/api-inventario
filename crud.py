from sqlalchemy.orm import Session
import models
import schemas

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