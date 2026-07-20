# 📖 Estudio Técnico — API de Inventario (Fases 1-5)

## Autor: Marcos Ramos

## Fecha: Julio 2025

# 📚 ÍNDICE

- [📖 Estudio Técnico — API de Inventario (Fases 1-5)](#-estudio-técnico--api-de-inventario-fases-1-5)
  - [Autor: Marcos Ramos](#autor-marcos-ramos)
  - [Fecha: Julio 2025](#fecha-julio-2025)
- [📚 ÍNDICE](#-índice)
- [1. Arquitectura general del proyecto](#1-arquitectura-general-del-proyecto)
  - [Estructura de archivos](#estructura-de-archivos)
  - [Flujo general de una petición](#flujo-general-de-una-petición)
  - [Flujo con autenticación](#flujo-con-autenticación)
- [2. ¿Qué hace cada archivo?](#2-qué-hace-cada-archivo)
- [3. database.py — La conexión a PostgreSQL](#3-databasepy--la-conexión-a-postgresql)
  - [Código completo](#código-completo)
  - [Explicación línea por línea](#explicación-línea-por-línea)
    - [`load_dotenv()`](#load_dotenv)
    - [`DATABASE_URL = os.getenv("DATABASE_URL")`](#database_url--osgetenvdatabase_url)
    - [`engine = create_engine(DATABASE_URL)`](#engine--create_enginedatabase_url)
    - [`SessionLocal = sessionmaker(...)`](#sessionlocal--sessionmaker)
    - [`Base = declarative_base()`](#base--declarative_base)
    - [`get_db()` — La función más importante](#get_db--la-función-más-importante)
- [4. models.py — Los modelos del ORM](#4-modelspy--los-modelos-del-orm)
  - [Código completo](#código-completo-1)
  - [Explicación detallada](#explicación-detallada)
    - [¿Qué es un modelo?](#qué-es-un-modelo)
    - [`__tablename__ = "productos"`](#__tablename__--productos)
  - [Tipos de columnas](#tipos-de-columnas)
  - [Parámetros de las columnas](#parámetros-de-las-columnas)
  - [¿Qué es `primary_key`?](#qué-es-primary_key)
    - [Productos](#productos)
  - [¿Qué es `index`?](#qué-es-index)
    - [Diferencia entre modelo Producto y Usuario](#diferencia-entre-modelo-producto-y-usuario)
- [5. schemas.py — Validación de datos con Pydantic](#5-schemaspy--validación-de-datos-con-pydantic)
  - [¿Qué es Pydantic?](#qué-es-pydantic)
  - [¿Por qué no usar los modelos directamente?](#por-qué-no-usar-los-modelos-directamente)
  - [Schemas de Producto](#schemas-de-producto)
    - [ProductoBase — Campos comunes](#productobase--campos-comunes)
      - [Significado de los parámetros de Field:](#significado-de-los-parámetros-de-field)
    - [ProductoCrear — Para crear (hereda de Base)](#productocrear--para-crear-hereda-de-base)
    - [ProductoActualizar — Todo opcional](#productoactualizar--todo-opcional)
    - [ProductoRespuesta — Lo que devuelve la API](#productorespuesta--lo-que-devuelve-la-api)
  - [Schemas de Usuario](#schemas-de-usuario)
    - [UsuarioCrear](#usuariocrear)
    - [UsuarioRespuesta](#usuariorespuesta)
    - [Token](#token)
- [6. crud.py — Operaciones a la base de datos](#6-crudpy--operaciones-a-la-base-de-datos)
  - [¿Qué es CRUD?](#qué-es-crud)
  - [Funciones de Producto](#funciones-de-producto)
    - [Crear producto](#crear-producto)
    - [Obtener todos los productos](#obtener-todos-los-productos)
    - [Obtener un producto por ID](#obtener-un-producto-por-id)
    - [Actualizar producto](#actualizar-producto)
    - [Eliminar producto](#eliminar-producto)
  - [Funciones de Usuario](#funciones-de-usuario)
    - [Obtener usuario por email](#obtener-usuario-por-email)
    - [Crear usuario](#crear-usuario)
- [7. auth.py — Hashing y JWT](#7-authpy--hashing-y-jwt)
  - [Código completo](#código-completo-2)
  - [Explicación detallada](#explicación-detallada-1)
    - [Variables de configuración](#variables-de-configuración)
- [8. dependencies.py — Protección de rutas](#8-dependenciespy--protección-de-rutas)
  - [Código completo](#código-completo-3)
  - [Explicación detallada](#explicación-detallada-2)
    - [¿Cómo se usa en un endpoint?](#cómo-se-usa-en-un-endpoint)
    - [¿Qué es `Depends()`?](#qué-es-depends)
- [9. routers/productos.py — Endpoints de productos](#9-routersproductospy--endpoints-de-productos)
  - [¿Qué es un Router?](#qué-es-un-router)
  - [Anatomía de un endpoint](#anatomía-de-un-endpoint)
  - [Endpoints públicos vs protegidos](#endpoints-públicos-vs-protegidos)
  - [¿Qué es `HTTPException`?](#qué-es-httpexception)
  - [¿Qué es `{producto_id}` en la ruta?](#qué-es-producto_id-en-la-ruta)
- [10. routers/auth.py — Endpoints de autenticación](#10-routersauthpy--endpoints-de-autenticación)
  - [Registro](#registro)
  - [Login](#login)
  - [¿Qué es `OAuth2PasswordRequestForm`?](#qué-es-oauth2passwordrequestform)
  - [¿Por qué el error dice "Email o contraseña incorrectos"?](#por-qué-el-error-dice-email-o-contraseña-incorrectos)
  - [¿Qué es "sub" en el token?](#qué-es-sub-en-el-token)
  - [Perfil del usuario actual](#perfil-del-usuario-actual)
- [11. main.py — Punto de entrada](#11-mainpy--punto-de-entrada)
- [12. Flujos completos paso a paso](#12-flujos-completos-paso-a-paso)
  - [Flujo 1: Registro de usuario](#flujo-1-registro-de-usuario)
  - [Flujo 2: Login](#flujo-2-login)
  - [Flujo 3: Crear producto (protegido)](#flujo-3-crear-producto-protegido)
  - [Flujo 4: Listar productos (público)](#flujo-4-listar-productos-público)
- [13. Conceptos clave explicados](#13-conceptos-clave-explicados)
  - [¿Qué es una sesión de base de datos?](#qué-es-una-sesión-de-base-de-datos)
  - [¿Qué es inyección de dependencias?](#qué-es-inyección-de-dependencias)
  - [¿Qué es hashing?](#qué-es-hashing)
  - [¿Qué es un salt?](#qué-es-un-salt)
  - [¿Qué es OAuth2?](#qué-es-oauth2)
- [14. Glosario técnico](#14-glosario-técnico)

***

# 1. Arquitectura general del proyecto

## Estructura de archivos

api-inventario/

├── .env → Variables secretas (contraseñas, claves)
\
├── .gitignore → Archivos que Git debe ignorar
\
├── main.py → Punto de entrada de la aplicación
\
├── database.py → Conexión a PostgreSQL
\
├── models.py → Definición de tablas (ORM)\
├── schemas.py → Validación de datos entrada/salida
\
├── crud.py → Funciones que hablan con la BD
\
├── auth.py → Lógica de contraseñas y tokens JWT
\
├── dependencies.py → Función que protege rutas
\
├── requirements.txt → Lista de librerías instaladas
\
├── routers/
\
│ ├── init.py → Marca la carpeta como módulo Python
\
│ ├── productos.py → Endpoints de productos
\
│ └── auth.py → Endpoints de autenticación
\
└── docs/
\
└── estudio-tecnico.md → Este documento

## Flujo general de una petición

CLIENTE (navegador, Swagger, Postman)
\
│
\
▼
\
main.py → Recibe la petición
\
│
\
▼
\
routers/\*.py → Decide qué función ejecutar
\
│
\
▼
\
schemas.py → Valida los datos de entrada
\
│
\
▼
\
crud.py → Ejecuta la operación en la BD
\
│
\
▼
\
models.py → Define la estructura de las tablas
\
│
\
▼
\
database.py → Maneja la conexión con PostgreSQL
\
│
\
▼
\
PostgreSQL → Almacena los datos

## Flujo con autenticación

CLIENTE envía token en el header
\
│
\
▼
\
dependencies.py → Extrae y valida el token
\
│
\
▼
\
auth.py → Decodifica el JWT
\
│
\
▼
\
crud.py → Busca al usuario en la BD
\
│
\
▼
\
Si es válido → ejecuta el endpoint
\
Si no → devuelve error 401

text

***

# 2. ¿Qué hace cada archivo?

| Archivo                | Responsabilidad                     | Analogía                             |
| ---------------------- | ----------------------------------- | ------------------------------------ |
| `main.py`              | Arranca la app, conecta todo        | El gerente del restaurante           |
| `database.py`          | Conexión a PostgreSQL               | La instalación eléctrica             |
| `models.py`            | Define las tablas con Python        | El plano del almacén                 |
| `schemas.py`           | Valida datos de entrada/salida      | El inspector de calidad              |
| `crud.py`              | Lee/escribe en la BD                | El cocinero                          |
| `auth.py`              | Hashea contraseñas, crea tokens     | El sistema de seguridad              |
| `dependencies.py`      | Verifica tokens en rutas protegidas | El guardia de seguridad              |
| `routers/productos.py` | Endpoints de productos              | El mesero de la sección de productos |
| `routers/auth.py`      | Endpoints de login/registro         | El mesero de la sección de acceso    |

***

# 3. database.py — La conexión a PostgreSQL

## Código completo

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Explicación línea por línea


### `load_dotenv()`

Lee el archivo `.env` y carga sus variables al entorno del sistema operativo.

Sin esto, `os.getenv("DATABASE\_URL")` devolvería `None`.

```text
.env contiene:
DATABASE_URL=postgresql://postgres:admin123@localhost:5432/inventario_db

Después de load_dotenv():
os.getenv("DATABASE_URL") → "postgresql://postgres:admin123@localhost:5432/inventario_db"
```

***

### `DATABASE_URL = os.getenv("DATABASE_URL")`

Obtiene la URL de conexión desde las variables de entorno.

La URL tiene este formato:

```text
postgresql://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BD
```

***

### `engine = create_engine(DATABASE_URL)`

Crea el "motor" de conexión a la base de datos.

- NO abre la conexión todavía
- Solo PREPARA la configuración
- Es como enchufar un cable a la pared (no prende nada aún)

***

### `SessionLocal = sessionmaker(...)`

Crea una "fábrica" de sesiones.

¿Qué es una sesión? Es una conversación temporal con la base de datos.

```text
Sesión = abrir conexión → hacer operaciones → cerrar conexión
```

Los parámetros:

- `autocommit=False` → No guardar automáticamente (nosotros decidimos cuándo con `db.commit()`)
- `autoflush=False` → No enviar cambios parciales a la BD
- `bind=engine` → Usa este motor de conexión

***

### `Base = declarative_base()`

Crea la clase padre de todos los modelos.

Cualquier modelo que herede de `Base` será convertido en tabla automáticamente.

```Python
class Producto(Base):  ← hereda de Base
__tablename__ = "productos"
```

### `get_db()` — La función más importante

```Python
def get_db():
    db = SessionLocal()    # 1. Abre una sesión
    try:
        yield db           # 2. La "presta" al endpoint
    finally:
        db.close()         # 3. La cierra cuando termina
```

¿Qué es `yield`?

`yield` es como `return`, pero NO termina la función. La "pausa" y después continúa.

Flujo:

1. El endpoint pide una sesión de BD
2. get\_db() crea una sesión y se la presta con yield
3. El endpoint hace su trabajo (queries, inserts, etc.)
4. Cuando el endpoint termina, get\_db() continúa
5. Ejecuta db.close() → cierra la sesión

Es como un bibliotecario:
d
- Te presta un libro (yield db)
- Tú lo lees (endpoint trabaja)
- Cuando terminas, él lo guarda (db.close())

# 4\. models.py — Los modelos del ORM

## Código completo

```python
from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    contraseña_hash = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)
```

## Explicación detallada

### ¿Qué es un modelo?

Un modelo es una clase de Python que representa una tabla en la base de datos.

Cada atributo de la clase = una columna de la tabla.

### `__tablename__ = "productos"`

Le dice a SQLAlchemy: "esta clase corresponde a la tabla llamada 'productos' en PostgreSQL".

## Tipos de columnas

| Python (SQLAlchemy)   | PostgreSQL     | Ejemplo       |
| --------------------- | -------------- | ------------- |
| `Column(Integer)`     | `INTEGER`      | id,stock      |
| `Column(String(100))` | `VARCHAR(100)` | nombre, email |
| `Column(Float)`       | `FLOAT`        | precio        |
| `Column(Boolean)`     | `BOOLEAN`      | activo        |

## Parámetros de las columnas

| Parámetro           | Significado                                | Ejemplo            |
| ------------------- | ------------------------------------------ | ------------------ |
| `primary_key=True`  | Es la clave primaria (identificador único) | `id`               |
| `index=True`        | Crea un índice para búsquedas rápidas      | `id`, `email`      |
| `nullable=False`    | NO puede ser NULL (obligatorio)            | `nombre`, `precio` |
| `nullable=True`     | Puede ser NULL (opcional)                  | `descripcion`      |
| `unique=True`       | No puede repetirse                         | `email`            |
| `default=0`         | Valor por defecto si no se envía           | `stock`            |

## ¿Qué es `primary_key`?

Es el identificador único de cada fila. Nunca se repite.

### Productos

| id  | nombre    | precio |
| --- | --------- | ------ |
| 1   | Laptop HP | 850.50 |
| 2   | Mouse     | 25.00  |
| 3   | Teclado   | 45.00  |

El id se genera automáticamente (autoincremental).

## ¿Qué es `index`?

Un índice es como el índice de un libro. Sin él, PostgreSQL buscaría fila por fila (lento). Con índice, va directo a la fila (rápido).

### Diferencia entre modelo Producto y Usuario

| Campo            | Producto | Usuario    |
| ---------------- | -------- | ---------- |
| id               | ✅        | ✅          |
| nombre           | ✅        | ✅          |
| email            | ❌        | ✅ (unique) |
| contraseña\_hash | ❌        | ✅          |
| precio           | ✅        | ❌          |
| stock            | ✅        | ❌          |
| descripcion      | ✅        | ❌          |
| activo           | ✅        | ✅          |

# 5\. schemas.py — Validación de datos con Pydantic

## ¿Qué es Pydantic?

Pydantic es una librería que valida datos automáticamente.

Si defines que `precio` debe ser `float` y mayor que 0, Pydantic rechazará automáticamente:

- precio: "hola" → Error (no es float)
- precio: -5 → Error (no es mayor que 0)
- precio: 25.50 → ✅ Válido

## ¿Por qué no usar los modelos directamente?
Los MODELOS (models.py) representan la BASE DE DATOS.

Los SCHEMAS (schemas.py) representan lo que el USUARIO envía/recibe.

No siempre coinciden:

```text
El usuario envía:
{
    "nombre": "Laptop",
    "precio": 850.50
}

La BD tiene:
id=1, nombre="Laptop", precio=850.50, stock=0, activo=true

La API responde:
{
    "id": 1,
    "nombre": "Laptop",
    "precio": 850.50,
    "stock": 0,
    "activo": true
}
```

- El usuario NO envía el id (lo genera la BD)
- La API SÍ devuelve el id
- La BD guarda contraseña\_hash, pero NUNCA se devuelve al usuario

Por eso hay schemas diferentes para entrada y salida.

## Schemas de Producto
### ProductoBase — Campos comunes

```Python
class ProductoBase(BaseModel):
nombre: str = Field(..., min_length=1, max_length=100)
descripcion: Optional[str] = Field(None, max_length=255)
precio: float = Field(..., gt=0)
stock: int = Field(default=0, ge=0)
activo: bool = True
```

| Campo       | Tipo       | Validación        | Obligatorio       |
| ----------- | ---------- | ----------------- | ----------------- |
| nombre      | str        | 1-100 caracteres  | Sí (`...`)        |
| descripcion | str o None | máx 255 chars     | No (`None`)       |
| precio      | float      | mayor que 0       | Sí (`...`)        |
| stock       | int        | mayor o igual a 0 | No (default 0)    |
| activo      | bool       | -                 | No (default True) |

#### Significado de los parámetros de Field:

- `...` → campo obligatorio
- `None` → campo opcional (default None)
- `min_length=1` → mínimo 1 carácter
- `max_length=100` → máximo 100 caracteres
- `gt=0` → greater than 0 (mayor que 0)
- `ge=0` → greater or equal 0 (mayor o igual a 0)

### ProductoCrear — Para crear (hereda de Base)

```python
class ProductoCrear(ProductoBase):
    pass
```

`pass` significa "no agrego nada, uso todo lo que tiene ProductoBase tal cual".

¿Por qué existe si es igual? Porque en el futuro podríamos añadir campos exclusivos para la creación sin modificar ProductoBase.

### ProductoActualizar — Todo opcional

```python
class ProductoActualizar(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None
```

Todos los campos son `Optional` porque al actualizar, el usuario puede enviar solo los campos que quiere modificar.

Ejemplo: solo cambiar el precio:

```JSON
{"precio": 999.99}
```

### ProductoRespuesta — Lo que devuelve la API
```python
class ProductoRespuesta(ProductoBase):
    id: int

    class Config:
        from_attributes = True
```

Hereda todos los campos de ProductoBase y AÑADE `id`.

`from_attributes = True` le dice a Pydantic: "los datos vienen de un objeto de SQLAlchemy (modelo), no de un diccionario, así que léelos como atributos".

Sin esto, Pydantic no sabría cómo convertir un objeto `Producto` de SQLAlchemy a JSON.

## Schemas de Usuario

### UsuarioCrear

```python
class UsuarioCrear(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=1, max_length=100)
    contraseña: str = Field(..., min_length=6, max_length=100)
```

`EmailStr` valida automáticamente que sea un email real:

`"<marcos@test.com>"` → ✅
`"marcos"` → ❌
`"marcos@"` → ❌

### UsuarioRespuesta

```python
class UsuarioRespuesta(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    activo: bool
```

NOTA IMPORTANTE: NO incluye `contraseña` ni `contraseña_hash`.
Nunca se devuelve la contraseña al usuario. Es una regla de seguridad básica.

### Token

```python
class Token(BaseModel):
    access_token: str
    token_type: str
```
Respuesta del login:

```JSON
{
"access\_token": "eyJhbGciOi...",
"token\_type": "bearer"
}
```

# 6\. crud.py — Operaciones a la base de datos

## ¿Qué es CRUD?

| Letra | Operación | Método HTTP | SQL    |
| ----- | --------- | ----------- | ------ |
| C     | Create    | POST        | INSERT |
| R     | Read      | GET         | SELECT |
| U     | Update    | PUT         | UPDATE |
| D     | Delete    | DELETE      | DELETE |

## Funciones de Producto

### Crear producto

```python
def crear_producto(db: Session, producto: schemas.ProductoCrear):
    nuevo_producto = models.Producto(**producto.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto
```

Paso a paso:

1. `producto.model_dump()` → Convierte el schema Pydantic a diccionario

    ```python
    {"nombre": "Laptop", "precio": 850.50, "stock": 10, "activo": True}
    ```

2. `models.Producto(**diccionario)` → Crea un objeto Producto usando ese diccionario

   - `**` es el operador de desempaquetado: pasa cada clave como parámetro
   - Es como hacer: `Producto(nombre="Laptop", precio=850.50, stock=10, activo=True)`

3. `db.add(nuevo_producto)` → Prepara el INSERT (aún no lo ejecuta)

4. `db.commit()` → Ejecuta el INSERT y guarda en la BD permanentemente

5. `db.refresh(nuevo_producto)` → Recarga el objeto desde la BD para obtener el `id` generado

6. `return nuevo_producto` → Devuelve el producto con su `id`

Equivalente SQL:

```SQL
INSERT INTO productos (nombre, precio, stock, activo)
VALUES ('Laptop', 850.50, 10, true)
RETURNING *;
```

### Obtener todos los productos

```python
def obtener_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()
```

- `db.query(models.Producto)` → `SELECT * FROM productos`
- `.offset(skip)` → salta las primeras N filas (paginación)
- `.limit(limit)` → máximo N resultados
- `.all()` → devuelve una lista con todos los resultados

Equivalente SQL:

```SQL
SELECT * FROM productos OFFSET 0 LIMIT 100;
```

### Obtener un producto por ID
```python
def obtener_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()
```
- `.filter(models.Producto.id == producto_id)` → `WHERE id = X`
- `.first()` → devuelve el primer resultado o `None` si no existe

Equivalente SQL:

```SQL
SELECT * FROM productos WHERE id = 1 LIMIT 1;
```

### Actualizar producto

```python
def actualizar_producto(db: Session, producto_id: int, datos: schemas.ProductoActualizar):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        return None

    datos_dict = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_dict.items():
        setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)
    return producto
```

Paso a paso:

1. Busca el producto por ID
2. Si no existe, devuelve `None`
3. `model_dump(exclude_unset=True)` → solo incluye los campos que el usuario envió
   - Si envió `{"precio": 999}`, solo devuelve `{"precio": 999}`
   - No incluye nombre, stock, etc. (no fueron enviados)
4. `setattr(producto, campo, valor)` → modifica dinámicamente el atributo
   - Es como hacer `producto.precio = 999`
5. `commit()` → guarda los cambios
6. `refresh()` → recarga desde BD

### Eliminar producto

```python
def eliminar_producto(db: Session, producto_id: int):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        return None
    db.delete(producto)
    db.commit()
    return producto
```

- Busca el producto
- Si no existe → None
- `db.delete()` → marca para eliminar
- `db.commit()` → ejecuta el DELETE

## Funciones de Usuario

### Obtener usuario por email

```python
def obtener_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()
```
Busca un usuario por su email. Se usa en:

- Registro (para verificar que no exista)
- Login (para encontrar al usuario)
- Validación de token (para obtener al usuario actual)

### Crear usuario

```python
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
```

DIFERENCIA CLAVE con crear\_producto:

No usamos `**model_dump()` porque el schema tiene `contraseña` pero el modelo tiene `contraseña_hash`. Son campos diferentes.

Flujo:

1. Hashea la contraseña (nunca guarda la original)
2. Crea el objeto Usuario manualmente (campo por campo)
3. Guarda en BD

# 7\. auth.py — Hashing y JWT

## Código completo
```python
import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_contraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)

def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool:
    return pwd_context.verify(contraseña_plana, contraseña_hash)

def crear_token_acceso(datos: dict) -> str:
    datos_copia = datos.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_copia.update({"exp": expira})
    return jwt.encode(datos_copia, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

## Explicación detallada

### Variables de configuración

```python
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
```

- `SECRET_KEY` → La clave secreta para firmar los tokens. Si alguien la conoce, puede crear tokens falsos.
- `ALGORITHM` → El algoritmo de encriptación. HS256 es el estándar.
- `ACCESS_TOKEN_EXPIRE_MINUTES` → Cuántos minutos dura el token antes de expirar.

`pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")`

Configura el sistema de hashing:

- `schemes=["bcrypt"]` → Usa el algoritmo bcrypt (el más seguro para contraseñas)
- `deprecated="auto"` → Si en el futuro cambias de algoritmo, marca los viejos como deprecados automáticamente

`hashear_contraseña(contraseña)`

```Python
def hashear_contraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)
```

Convierte una contraseña en texto plano a un hash irreversible.

```text
"123456" → "$2b$12\$LJ3m4ys3MnQB7kE5g6Oqj.1T..."
```

Cada vez que ejecutas esta función con la misma contraseña, genera un hash DIFERENTE (por el "salt" aleatorio). Pero `verificar_contraseña` puede compararlos correctamente.

`verificar_contraseña(plana, hash)`

```python
def verificar_contraseña(contraseña_plana: str, contraseña_hash: str) -> bool:
    return pwd_context.verify(contraseña_plana, contraseña_hash)
```

Compara una contraseña en texto plano con un hash.

```text
verify("123456", "$2b$12$LJ3m4...") → True
verify("654321", "$2b$12$LJ3m4...") → False
```

No "des-hashea" (es imposible). Hashea la contraseña nueva y compara los resultados.

`crear_token_acceso(datos)`

```python
def crear_token_acceso(datos: dict) -> str:
    datos_copia = datos.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_copia.update({"exp": expira})
    return jwt.encode(datos_copia, SECRET_KEY, algorithm=ALGORITHM)
```

Paso a paso:

1. Recibe datos (ejemplo: `{"sub": "<marcos@test.com>"}`)
2. Copia los datos (no modifica el original)
3. Calcula la fecha de expiración (ahora + 60 minutos)
4. Añade `"exp"` al diccionario
5. Codifica todo con la SECRET\_KEY y el algoritmo HS256
6. Devuelve el token como string

El token resultante tiene 3 partes separadas por puntos:

```text
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYXJjb3NAdGVzdC5jb20iLCJleHAiOjE3MDAwMDB9.firma
HEADER          .              PAYLOAD                              . SIGNATURE
```

- HEADER: {"alg": "HS256", "typ": "JWT"} (codificado en base64)
- PAYLOAD: {"sub": "<marcos@test.com>", "exp": 1700000} (codificado en base64)
- SIGNATURE: firma criptográfica usando SECRET\_KEY

⚠️ El payload NO está encriptado, solo codificado en base64. Cualquiera puede leerlo.
La FIRMA es lo que garantiza que nadie lo modificó.

`decodificar_token(token)`

```python
def decodificar_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

1. Recibe el token string
2. Intenta decodificarlo con la misma SECRET\_KEY
3. Si es válido y no expiró → devuelve el payload (diccionario)
4. Si es inválido, modificado o expirado → devuelve None

Posibles errores que captura JWTError:

- Token modificado (firma no coincide)
- Token expirado
- Token mal formado
- SECRET\_KEY diferente

# 8\. dependencies.py — Protección de rutas

## Código completo

```python

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from auth import decodificar_token
import crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

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
```

## Explicación detallada

`OAuth2PasswordBearer(tokenUrl="/auth/login")`

Le dice a FastAPI:

- "Los tokens se obtienen en la ruta /auth/login"
- "Espera el token en el header: `Authorization: Bearer <token>"`
- Esto también configura el botón "Authorize" en Swagger

`obtener_usuario_actual()` — El guardia de seguridad

Esta función se ejecuta ANTES de cada endpoint protegido.

Flujo:

1. FastAPI extrae el token del header Authorization

   ↓

2. Depends(oauth2\_scheme) se lo pasa como parámetro "token"

   ↓

3. decodificar\_token(token) lo valida

   ↓

4. Si es None → token inválido → error 401

   ↓

5. Extrae el email del payload (campo "sub")

   ↓

6. Si no hay email → error 401

   ↓

7. Busca al usuario en la BD por email

   ↓

8. Si no existe → error 401

   ↓

9.  Si todo OK → devuelve el objeto usuario
   
### ¿Cómo se usa en un endpoint?
```python
@router.post("/")
def crear_producto(
    producto: schemas.ProductoCrear,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)  # ← AQUÍ
):
```

`Depends(obtener_usuario_actual)` activa la cadena de validación.
Si el token no es válido, el endpoint NUNCA se ejecuta.

### ¿Qué es `Depends()`?

Es el sistema de "inyección de dependencias" de FastAPI.

Significa: "antes de ejecutar esta función, ejecuta esta otra y dame su resultado".

Cadena de dependencias:

```text
Depends(obtener_usuario_actual)
└── Depends(oauth2_scheme)     → extrae token del header
└── Depends(get_db)            → abre sesión de BD
```

FastAPI resuelve toda la cadena automáticamente.

# 9\. routers/productos.py — Endpoints de productos

## ¿Qué es un Router?

Es una forma de agrupar endpoints relacionados en un archivo separado.

```python
router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)
```

- `prefix="/productos"` → todas las rutas empiezan con `/productos`
  - `@router.get("/")` se convierte en `GET /productos/`
  - `@router.get("/{id}")` se convierte en `GET /productos/{id}`
- `tags=["Productos"]` → en Swagger, aparecen bajo la etiqueta "Productos"

## Anatomía de un endpoint

```python
@router.post("/", response_model=schemas.ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_producto(
    producto: schemas.ProductoCrear,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    return crud.crear_producto(db=db, producto=producto)
```

Desglose:

| Parte                                                 |	Significado                             |
| ----------------------------------------------------- | ----------------------------------------- |
| `@router.post("/") `                                  |	Método POST en la ruta /productos/      |
| `response_model=schemas.ProductoRespuesta`            |	La respuesta tendrá esta forma          |
| `status_code=status.HTTP_201_CREATED`                 |	Código de respuesta: 201                |
| `producto: schemas.ProductoCrear`                     |	Recibe JSON validado por Pydantic       |
| `db: Session = Depends(get_db)`                       |	Inyecta una sesión de BD                |
| `usuario_actual = Depends(obtener_usuario_actual)`    |	Requiere token                          |
| `return crud.crear_producto(...)`                     |	Delega la lógica a crud.py              |

## Endpoints públicos vs protegidos

```python

# PÚBLICO (no tiene Depends(obtener_usuario_actual))

@router.get("/")
def listar_productos(db: Session = Depends(get_db)):
    ...

# PROTEGIDO (sí tiene Depends(obtener_usuario_actual))

@router.post("/")
def crear_producto(
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)  # ← esto lo protege
):
    ...
```

La diferencia es UNA línea: `Depends(obtener_usuario_actual)`.

Si está → requiere token.
Si no está → es público.

## ¿Qué es `HTTPException`?

```Python
if not producto:
    raise HTTPException(status_code=404, detail="Producto no encontrado")
```

`raise` lanza una excepción que FastAPI captura y convierte en respuesta HTTP:

```JSON
HTTP 404
{
    "detail": "Producto no encontrado"
}
```

## ¿Qué es `{producto_id}` en la ruta?

```Python
@router.get("/{producto\_id}")
def obtener\_producto(producto\_id: int, ...):
```

Es un "parámetro de ruta" (path parameter).

```text
GET /productos/5
               └── producto\_id = 5
```

FastAPI extrae automáticamente el `5` de la URL y lo pasa como argumento `producto_id` a la función.

# 10\. routers/auth.py — Endpoints de autenticación

## Registro

```Python
@router.post("/registro", response_model=schemas.UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    usuario_existente = crud.obtener_usuario_por_email(db, email=usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este email ya está registrado")
    return crud.crear_usuario(db=db, usuario=usuario)
```

Flujo:

1. Recibe email, nombre, contraseña
2. Busca si el email ya existe
3. Si existe → error 400
4. Si no existe → crea el usuario (con contraseña hasheada)
5. Devuelve el usuario (sin contraseña)

## Login

```Python
@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = crud.obtener_usuario_por_email(db, email=form_data.username)
    if not usuario or not verificar_contraseña(form_data.password, usuario.contraseña_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    token = crear_token_acceso(datos={"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}
```

## ¿Qué es `OAuth2PasswordRequestForm`?

Es un formulario estándar de OAuth2 que tiene dos campos:

- `username` (nosotros lo usamos como email)
- `password`

Swagger lo reconoce automáticamente y muestra el formulario en el botón "Authorize".

## ¿Por qué el error dice "Email o contraseña incorrectos"?

Por seguridad. NUNCA decimos "el email no existe" o "la contraseña es incorrecta" por separado.

Si dijéramos "email no existe", un atacante podría probar emails hasta encontrar uno válido. Dando un mensaje genérico, no sabe cuál de los dos está mal.

## ¿Qué es "sub" en el token?

```Python
token = crear_token_acceso(datos={"sub": usuario.email})
```

`"sub"` viene de "subject" (sujeto). Es un estándar de JWT que indica "de quién es este token".

Nosotros usamos el email como subject.

## Perfil del usuario actual

```Python
@router.get("/yo", response_model=schemas.UsuarioRespuesta)
def obtener_mi_perfil(usuario_actual: models.Usuario = Depends(obtener_usuario_actual)):
    return usuario_actual
```

Este endpoint es protegido.
Simplemente devuelve el usuario que corresponde al token enviado.
Es útil para que el frontend sepa "quién está logueado".

# 11\. main.py — Punto de entrada

```Python
from fastapi import FastAPI
from database import engine
import models
from routers import productos, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Inventario",
    description="API REST para gestionar productos con autenticación JWT",
    version="0.3.0"
)

app.include_router(auth.router)
app.include_router(productos.router)

@app.get("/")
def root():
    return {"mensaje": "¡Bienvenido a la API de Inventario! 🚀"}

@app.get("/salud")
def salud():
    return {"estado": "ok", "servicio": "api-inventario"}
```

`models.Base.metadata.create_all(bind=engine)`

Lee TODOS los modelos que heredan de `Base` (Producto y Usuario) y crea las tablas en PostgreSQL si no existen.

Equivale a ejecutar:

```SQL
CREATE TABLE IF NOT EXISTS productos (...);
CREATE TABLE IF NOT EXISTS usuarios (...);
```

`app.include_router(auth.router)`

Conecta el router de auth a la app principal.
Todas las rutas de `routers/auth.py` se añaden bajo el prefijo `/auth`.

`app.include\_router(productos.router)`

Conecta el router de productos.
Todas las rutas se añaden bajo el prefijo `/productos`.

# 12\. Flujos completos paso a paso
   
## Flujo 1: Registro de usuario

```text

CLIENTE                         SERVIDOR
│                               │
│  POST /auth/registro          │
│  {email, nombre, contraseña}  │
│ ─────────────────────────────►│
│                               │
│              schemas.py valida los datos
│              crud.py busca si el email existe
│              Si existe → error 400
│              Si no → hashea contraseña
│              Guarda en tabla "usuarios"
│                               │
│  201 Created                  │
│  {id, email, nombre, activo}  │
│ ◄─────────────────────────────│

```

## Flujo 2: Login

```text

CLIENTE                         SERVIDOR
│                               │
│  POST /auth/login             │
│  username=email               │
│  password=contraseña          │
│ ─────────────────────────────►│
│                               │
│              Busca usuario por email
│              Compara contraseña con hash
│              Si no coincide → error 401
│              Si coincide → genera JWT
│                               │
│  200 OK                       │
│  {access\_token, token\_type}   │
│ ◄─────────────────────────────│

```

## Flujo 3: Crear producto (protegido)

```text

CLIENTE                         SERVIDOR
│                               │
│  POST /productos/             │
│  Header: Authorization:       │
│    Bearer eyJhbG...           │
│  Body: {nombre, precio...}    │
│ ─────────────────────────────►│
│                               │
│         dependencies.py extrae token
│         auth.py decodifica token
│         crud.py busca usuario por email del token
│         Si token inválido → error 401
│         Si válido → schemas.py valida el body
│         crud.py inserta en tabla "productos"
│                               │
│  201 Created                  │
│  {id, nombre, precio...}      │
│ ◄─────────────────────────────│

```

## Flujo 4: Listar productos (público)

```text

CLIENTE                         SERVIDOR
│                               │
│  GET /productos/              │
│  (sin token)                  │
│ ─────────────────────────────►│
│                               │
│         No requiere autenticación
│         crud.py consulta tabla "productos"
│                               │
│  200 OK                       │
│  \[{producto1}, {producto2}]   │
│ ◄─────────────────────────────│

```

# 13\. Conceptos clave explicados

## ¿Qué es una sesión de base de datos?

Es una conexión temporal entre tu código Python y PostgreSQL.

```text
Abrir sesión → Hacer operaciones → Cerrar sesión
```

Es como una llamada telefónica:

- Marcas el número (abrir sesión)
- Hablas (queries)
- Cuelgas (cerrar sesión)

Si no cierras la sesión, dejas la línea ocupada y eventualmente se acaban las conexiones disponibles.

## ¿Qué es inyección de dependencias?

Es cuando una función recibe automáticamente lo que necesita para trabajar.

Sin inyección:

```Python
def crear_producto():
    db = conectar_bd()           # tú la creas
    token = extraer_token()      # tú lo extraes
    usuario = validar_token()    # tú lo validas
    # ...
    db.close()                   # tú la cierras
```

Con inyección (Depends):

```Python
def crear_producto(
    db = Depends(get_db),                          # FastAPI te la da
    usuario = Depends(obtener_usuario_actual)       # FastAPI te lo da
):
    # solo te preocupas por la lógica
```

FastAPI se encarga de crear, inyectar y limpiar las dependencias.

## ¿Qué es hashing?

Es una función matemática que convierte cualquier dato en una cadena de longitud fija.

Propiedades:

- Irreversible (no puedes obtener el original)
- Determinista (la misma entrada siempre produce el mismo hash... casi, bcrypt añade salt)
- Pequeños cambios producen hashes completamente diferentes

```text
"123456"  → "$2b$12$abc..."
"123457"  → "$2b$12$xyz..."   (completamente diferente)
```

## ¿Qué es un salt?

Es un valor aleatorio que se añade a la contraseña antes de hashearla.

Sin salt:

```text
"123456" → siempre el mismo hash
```

Con salt:

```text
"123456" + salt_aleatorio_1 → hash_A
"123456" + salt_aleatorio_2 → hash_B
```

Bcrypt genera y almacena el salt automáticamente dentro del hash.

Esto protege contra ataques de "tablas rainbow" (diccionarios precalculados de hashes).

## ¿Qué es OAuth2?

Es un estándar de autorización que define cómo obtener y usar tokens de acceso.

Nosotros usamos el flujo "Password" (el más simple):

1. El usuario envía credenciales (email + contraseña)
2. El servidor valida y devuelve un token
3. El usuario usa el token para acceder a recursos protegidos

# 14\. Glosario técnico

| Término                   | Definición                                                    |
| ------------------------- | ------------------------------------------------------------- |
| API	                    | Interfaz que permite a programas comunicarse entre sí         |
| REST	                    | Estilo de arquitectura para APIs usando HTTP                  |
| Endpoint	                | Una URL específica de la API + un método HTTP                 |
| ORM	                    | Traductor entre objetos de Python y tablas SQL                |
| Schema	                | Definición de la forma que deben tener los datos              |
| Modelo	                | Clase Python que representa una tabla de BD                   |
| Sesión	                | Conexión temporal con la base de datos                        |
| Hash	                    | Transformación irreversible de datos                          |
| Salt	                    | Valor aleatorio añadido antes de hashear                      |
| JWT	                    | Token firmado digitalmente para autenticación                 |
| Payload	                | Contenido del token (datos del usuario)                       |
| Signature          	    | Firma criptográfica del token                                 |
| Bearer	                | Tipo de autenticación que usa tokens                          |
| Depends	                | Sistema de inyección de dependencias de FastAPI               |
| Middleware	            | Código que se ejecuta entre la petición y la respuesta        |
| CRUD	                    | Create, Read, Update, Delete                                  |
| Pydantic	                | Librería de validación de datos                               |
| SQLAlchemy	            | ORM para Python                                               |
| bcrypt	                | Algoritmo de hashing para contraseñas                         |
| Uvicorn	                | Servidor ASGI que ejecuta FastAPI                             |
| ASGI	                    | Estándar para servidores Python asíncronos                    |