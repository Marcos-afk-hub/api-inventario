from pydantic import BaseModel, Field
from typing import Optional

#Schema base con los campos comunes
class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    activo: bool = True

#Schema para CREAR un producto (entrada)
class ProductoCrear(ProductoBase):
    pass

#Schema para ACTUALIZAR un producto (todos los campos opcionales)
class ProductoActualizar (BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None

#Schema para RESPUESTA (salida)
class ProductoRespuesta(ProductoBase):
    id: int

    class Config:
        from_attributes = True    