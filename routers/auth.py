from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db
from auth import verificar_contraseña, crear_token_acceso
from dependencies import obtener_usuario_actual
import models

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post("/registro", response_model=schemas.UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    usuario_existente = crud.obtener_usuario_por_email(db, email=usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este email ya está registrado")
    return crud.crear_usuario(db=db, usuario=usuario)


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # OAuth2 usa "username", pero nosotros lo tratamos como email
    usuario = crud.obtener_usuario_por_email(db, email=form_data.username)
    if not usuario or not verificar_contraseña(form_data.password, usuario.contraseña_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    token = crear_token_acceso(datos={"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/yo", response_model=schemas.UsuarioRespuesta)
def obtener_mi_perfil(usuario_actual: models.Usuario = Depends(obtener_usuario_actual)):
    return usuario_actual