#!/bin/bash
set -e

# Si no existe la carpeta /app/django, la creamos
if [ ! -d /app/django ]; then
  echo ">> Creando carpeta /app/django ..."
  mkdir -p /app/django
fi

# Si no existe manage.py, significa que no hay proyecto, entonces lo creamos
if [ ! -f /app/django/manage.py ]; then
  echo ">> Proyecto Django no encontrado, creando en /app/django ..."
  django-admin startproject lineamientos /app/django
  python /app/django/manage.py migrate
fi

# Levantamos el servidor
echo ">> Iniciando servidor Django ..."
python /app/django/manage.py runserver 0.0.0.0:8000
