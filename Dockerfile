FROM python:3.9-slim

# Instalar dependencias del sistema necesarias para Python, Node y MySQL
RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    default-libmysqlclient-dev \
    gcc \
    g++ \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js 16
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

WORKDIR /app

COPY package*.json /app/
COPY . /app/

RUN npm install

# Instalar dependencias de Python (incluye mysqlclient)
RUN pip install --no-cache-dir -r requirements.txt

# Compila SCSS en CSS
ARG NODE_ENV=development
RUN if [ "$NODE_ENV" = "production" ]; then npm run build; else npm run build-dev; fi

EXPOSE 8000

CMD ["bash", "-c", "/app/start.sh"]
