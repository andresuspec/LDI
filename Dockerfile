FROM python:3.9-slim

# Instala Node.js, npm y dependencias python
RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Instala Node.js 16 (o la versión que quieras)
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

WORKDIR /app

COPY package*.json /app/
COPY . /app/

RUN npm install

RUN pip install --no-cache-dir -r requirements.txt

# Compila el SCSS en CSS
ARG NODE_ENV=development
RUN if [ "$NODE_ENV" = "production" ]; then npm run build; else npm run build-dev; fi


EXPOSE 8000

CMD ["bash", "-c", "/app/start.sh"]
