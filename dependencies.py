from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from auth import decodificar_token
import crud

# Le decimos a FastAPI que espere el token en el header Authorization: Bearer xxx
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Valida el token y devuelve el usuario actual"""
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decodificar_token(token)
    if payload is None:
        raise credenciales_invalidas

    email: str = payload.get("sub")
    if email is None:
        raise credenciales_invalidas

    usuario = crud.obtener_usuario_por_email(db, email=email)
    if usuario is None:
        raise credenciales_invalidas

    return usuario
