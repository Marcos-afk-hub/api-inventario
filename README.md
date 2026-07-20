# 🗄️ API de Inventario

API REST desarrollada con **FastAPI** y **PostgreSQL** para la gestión de productos en un sistema de inventario, con autenticación JWT y arquitectura modular profesional.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![JWT](https://img.shields.io/badge/Auth-JWT-black?logo=jsonwebtokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Tabla de contenido

- [🗄️ API de Inventario](#️-api-de-inventario)
  - [📋 Tabla de contenido](#-tabla-de-contenido)
  - [📝 Descripción](#-descripción)
  - [✨ Características](#-características)
  - [🛠️ Stack tecnológico](#️-stack-tecnológico)
  - [📂 Estructura del proyecto](#-estructura-del-proyecto)
  - [📋 Requisitos previos](#-requisitos-previos)
  - [🚀 Instalación](#-instalación)
    - [1. Clonar el repositorio](#1-clonar-el-repositorio)
    - [2. Crear entorno virtual](#2-crear-entorno-virtual)
    - [3. Activar el entorno virtual](#3-activar-el-entorno-virtual)
    - [4. Instalar dependencias](#4-instalar-dependencias)
    - [5. Crear la base de datos en PostgreSQL](#5-crear-la-base-de-datos-en-postgresql)
  - [⚙️ Configuración](#️-configuración)
  - [▶️ Ejecución](#️-ejecución)
  - [🛣️ Endpoints disponibles](#️-endpoints-disponibles)
    - [🌐 Rutas públicas](#-rutas-públicas)
    - [🔒 Rutas protegidas (requieren token JWT)](#-rutas-protegidas-requieren-token-jwt)
  - [🔐 Autenticación](#-autenticación)
    - [Flujo de autenticación](#flujo-de-autenticación)
  - [💡 Ejemplos de uso](#-ejemplos-de-uso)
    - [Registrar un usuario](#registrar-un-usuario)
    - [Iniciar sesión (obtener token)](#iniciar-sesión-obtener-token)
    - [Crear un producto (protegido)](#crear-un-producto-protegido)
    - [Listar productos (público)](#listar-productos-público)
  - [📚 Documentación interactiva](#-documentación-interactiva)
  - [🗺️ Roadmap](#️-roadmap)
    - [✅ Completado](#-completado)
    - [🚧 En desarrollo](#-en-desarrollo)
    - [🔮 Futuro](#-futuro)
  - [👤 Autor](#-autor)
  - [📄 Licencia](#-licencia)
  - [🙌 Agradecimientos](#-agradecimientos)

---

## 📝 Descripción

Esta API permite gestionar un inventario de productos de manera segura y escalable.  
Incluye un sistema de autenticación basado en **JSON Web Tokens (JWT)** que protege los endpoints sensibles (crear, actualizar y eliminar productos), mientras deja abiertos al público los endpoints de solo lectura.

El proyecto fue desarrollado siguiendo buenas prácticas de arquitectura backend:

- Separación clara de responsabilidades
- Validación robusta de datos con Pydantic
- ORM para abstracción de la base de datos
- Configuración mediante variables de entorno
- Documentación automática con Swagger UI

---

## ✨ Características

- 🔐 **Autenticación JWT** con contraseñas hasheadas usando bcrypt
- 📦 **CRUD completo** de productos
- 👤 **Gestión de usuarios**: registro, login y consulta de perfil
- 🛡️ **Endpoints protegidos** mediante inyección de dependencias
- ✅ **Validación automática** de datos con Pydantic
- 📚 **Documentación interactiva** con Swagger UI y ReDoc
- 🔧 **Arquitectura modular** con separación por responsabilidades
- 🗄️ **Persistencia** en PostgreSQL mediante SQLAlchemy ORM
- 🌐 **Variables de entorno** para configuración segura

---

## 🛠️ Stack tecnológico

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3.12 |
| Framework | FastAPI |
| Servidor ASGI | Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Base de datos | PostgreSQL 17 |
| Validación | Pydantic v2 |
| Autenticación | JWT (python-jose) |
| Hashing | bcrypt (passlib) |
| Gestión de env | python-dotenv |

---

## 📂 Estructura del proyecto

```
api-inventario/
├── .env                    # Variables de entorno (no se sube al repo)
├── .gitignore              # Archivos ignorados por Git
├── main.py                 # Punto de entrada de la aplicación
├── database.py             # Configuración de conexión a PostgreSQL
├── models.py               # Modelos ORM (Producto, Usuario)
├── schemas.py              # Validación de datos entrada/salida
├── crud.py                 # Operaciones a la base de datos
├── auth.py                 # Lógica de hashing y JWT
├── dependencies.py         # Dependencias reutilizables (auth)
├── requirements.txt        # Dependencias del proyecto
├── routers/
│   ├── __init__.py
│   ├── productos.py        # Endpoints de productos
│   └── auth.py             # Endpoints de autenticación
└── docs/
    └── estudio-tecnico.md  # Documentación técnica detallada
```

---

## 📋 Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10 o superior** → [Descargar](https://www.python.org/downloads/)
- **PostgreSQL 15 o superior** → [Descargar](https://www.postgresql.org/download/)
- **Git** → [Descargar](https://git-scm.com/downloads)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Marcos-afk-hub/api-inventario.git
cd api-inventario
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Crear la base de datos en PostgreSQL

Conéctate a PostgreSQL:

```bash
psql -U postgres
```

Crea la base de datos:

```sql
CREATE DATABASE inventario_db;
\q
```

---

## ⚙️ Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos
DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/inventario_db

# JWT
SECRET_KEY=tu-clave-super-secreta-larga-y-aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> ⚠️ **Importante:** Nunca subas tu archivo `.env` al repositorio. Ya está incluido en el `.gitignore`.

---

## ▶️ Ejecución

Con el entorno virtual activado, ejecuta:

```bash
uvicorn main:app --reload
```

La API estará disponible en:

```
http://127.0.0.1:8000
```

---

## 🛣️ Endpoints disponibles

### 🌐 Rutas públicas

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Mensaje de bienvenida |
| `GET` | `/salud` | Verifica el estado del servicio |
| `GET` | `/productos/` | Lista todos los productos |
| `GET` | `/productos/{id}` | Obtiene un producto específico |
| `POST` | `/auth/registro` | Registra un nuevo usuario |
| `POST` | `/auth/login` | Inicia sesión y devuelve un token JWT |

### 🔒 Rutas protegidas (requieren token JWT)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/auth/yo` | Obtiene el perfil del usuario autenticado |
| `POST` | `/productos/` | Crea un nuevo producto |
| `PUT` | `/productos/{id}` | Actualiza un producto existente |
| `DELETE` | `/productos/{id}` | Elimina un producto |

---

## 🔐 Autenticación

Esta API utiliza autenticación basada en **JWT (JSON Web Tokens)** con el esquema **OAuth2 Password Bearer**.

### Flujo de autenticación

```
1. Usuario se registra    → POST /auth/registro
2. Usuario hace login     → POST /auth/login
3. Servidor devuelve token JWT
4. Usuario envía token en el header:
   Authorization: Bearer <token>
5. Servidor valida el token y permite el acceso
```

Las contraseñas se almacenan hasheadas con **bcrypt** y nunca se devuelven en las respuestas.

---

## 💡 Ejemplos de uso

### Registrar un usuario

```bash
curl -X POST http://127.0.0.1:8000/auth/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "marcos@example.com",
    "nombre": "Marcos",
    "contraseña": "12345678"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "email": "marcos@example.com",
  "nombre": "Marcos",
  "activo": true
}
```

---

### Iniciar sesión (obtener token)

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=marcos@example.com&password=12345678"
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Crear un producto (protegido)

```bash
curl -X POST http://127.0.0.1:8000/productos/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop HP",
    "descripcion": "Laptop HP Pavilion 15",
    "precio": 850.50,
    "stock": 10,
    "activo": true
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "nombre": "Laptop HP",
  "descripcion": "Laptop HP Pavilion 15",
  "precio": 850.50,
  "stock": 10,
  "activo": true
}
```

---

### Listar productos (público)

```bash
curl http://127.0.0.1:8000/productos/
```

---

## 📚 Documentación interactiva

FastAPI genera automáticamente documentación interactiva. Una vez el servidor esté corriendo, accede a:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Desde Swagger UI puedes probar todos los endpoints sin necesidad de herramientas externas.

---

## 🗺️ Roadmap

### ✅ Completado

- [x] Setup del proyecto y entorno virtual
- [x] Configuración básica de FastAPI
- [x] Conexión a PostgreSQL con SQLAlchemy
- [x] CRUD completo de productos
- [x] Autenticación JWT con bcrypt
- [x] Estructura modular con routers
- [x] Documentación técnica

### 🚧 En desarrollo

- [ ] Documentación profesional (README + docstrings)
- [ ] Deploy en Render.com o Railway.app

### 🔮 Futuro

- [ ] Roles y permisos (admin / user)
- [ ] Categorías de productos
- [ ] Sistema de logs
- [ ] Tests unitarios con pytest
- [ ] Migraciones con Alembic
- [ ] Rate limiting
- [ ] Dockerización

---

## 👤 Autor

**Marcos Ramos**

- GitHub: [@Marcos-afk-hub](https://github.com/Marcos-afk-hub)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 🙌 Agradecimientos

Proyecto desarrollado como parte de mi aprendizaje de desarrollo backend con Python.

Si te resultó útil o quieres contribuir, ¡no dudes en dar una ⭐ o hacer un fork!
