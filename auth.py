import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_contraseña(contraseña: str) -> str:
    """Conversion de hashear contraseña plana"""
    return pwd_context.hash(contraseña)

def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool:
    """Comparacion de contraseña con hash"""
    return pwd_context.verify(contraseña_plana, contraseña_hash)

def crear_token_acceso(datos: dict) -> str:
    """Genera un JWT con los datos del usuario"""
    datos_copia = datos.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_copia.update({"exp": expira})
    return jwt.encode(datos_copia, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict | None:
    """Validacion del token, devolucion de contenido (o None si es invalido)"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None