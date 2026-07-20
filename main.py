from fastapi import FastAPI
from database import engine
import models
from routers import productos, auth

#Crea las tablas en la base de datos (si no existen)
models.Base.metadata.create_all(bind=engine)

#Now we create an instance to our application  
app = FastAPI(
    title="Inventory API",
    description="API REST to inventory products management",
    version="0.3.0"
)

#Incluimos el router de productos
app.include_router(auth.router)
app.include_router(productos.router)

#First PATH
@app.get("/")
def root ():
    return {"message": "¡Welcome to Inventory API!"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-inventario"}