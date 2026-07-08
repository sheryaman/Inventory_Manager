# Store API - Gestión de Inventario

API REST desarrollada con FastAPI y SQLAlchemy para la gestión de productos e inventario.

## Tecnologías Utilizadas
- **Python**
- **FastAPI**
- **SQLAlchemy** (ORM)
- **PostgreSQL** (producción) / SQLite (desarrollo)
- **Docker** & Docker Compose

## Local Development

1. Clona el repositorio
   ```bash
   git clone https://github.com/tuusuario/tu-repo.git
   cd tu-repo

Instala las dependenciasBashpip install -r requirements.txt
Configura las variables de entornoBashcp .env.example .env
# Edita el archivo .env con tus credenciales de base de datos
Ejecuta la APIBashuvicorn main:app --reload
Abre en tu navegador:
Documentación: http://127.0.0.1:8000/docs


Docker Deployment

Construye y levanta los contenedoresBashdocker-compose up --build
La API estará disponible en: http://localhost:8000

Endpoints Principales

GET /products → Obtener todos los productos
POST /products → Crear nuevo producto
PUT /products/{name}/stock → Actualizar stock
DELETE /products/{name} → Eliminar producto
POST /categories → Crear categoría

Estructura del Proyecto

main.py → Archivo principal de FastAPI
models.py → Modelos de SQLAlchemy
docker-compose.yml & Dockerfile → Configuración Docker
