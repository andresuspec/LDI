# Proyecto Django con Docker

Este repositorio contiene un proyecto **Django** que se ejecuta dentro de **contenedores Docker**.  
La imagen se construye desde cero e instala todas las dependencias listadas en `requirements.txt`.

---

## 📂 Estructura del proyecto

LDI/
├── Dockerfile # Imagen base con Python + dependencias
├── docker-compose.yml # Configuracion de servicios Docker
├── requirements.txt # Lista de dependencias de Django y librerías
├── django/manage.py # Script principal de Django
├── django/app/ # Código fuente del proyecto
    ├── init.py
    ├── settings.py # Configuración de Django
    ├── urls.py # Rutas principales
    ├── wsgi.py # Entrada WSGI
    ├── wsgi.py # Entrada WSGI
├── nginx/nginx.conf # Configuración del nginx
├── start.sh # Script para crear el django en caso que no exista


---

## 🚀 Requisitos previos

- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/) *(opcional si quieres usar base de datos en contenedor)*  

---

## 🛠️ Construcción y ejecución
docker compose up --build -d

### 1. Clonar el repositorio
```bash
git clone git@github.com:andresuspec/LDI.git
cd LDI
