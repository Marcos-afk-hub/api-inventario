from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

#CREAR producto
@router.post("/", response_model=schemas.ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: schemas.ProductoCrear, db: Session = Depends(get_db)):
    return crud.crear_producto(db=db, producto=producto)

#LISTAR productos
@router.get("/", response_model=List[schemas.ProductoRespuesta])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obtener_productos(db=db, skip=skip, limit=limit)

#OBTENER un producto por ID
@router.get("/{producto_id}", response_model=schemas.ProductoRespuesta)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.obtener_producto(db=db, producto_id=producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

#ELIMINAR producto
@router.delete("/{producto_id}", status_code=status.HTTP_200_OK)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.eliminar_producto(db=db, producto_id=producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": f"Producto {producto_id} eliminado correctamente"}