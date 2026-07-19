import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carga de variables, archivo .env
load_dotenv()

# Leemos la URL de conexion desde .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Creamos el motor de conexion
engine = create_engine(DATABASE_URL)

# Creamos una frabrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para nuestros modelos
Base = declarative_base()

#Funcion que nos dara una sesion por cada peticion
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()