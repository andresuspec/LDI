# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Instala las dependencias necesarias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia todos los archivos del proyecto
COPY . /app/

# Da permisos de ejecución al script start.sh
RUN chmod +x /app/start.sh

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para el servidor Django
EXPOSE 8000

# Comando por defecto (esto se puede modificar en docker-compose)
CMD ["bash", "-c", "/app/start.sh"]
