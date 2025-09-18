import requests
import json
import os

# Configuración de Forge
FORGE_CLIENT_ID = "iZd9khRS4OEAz5L0zqOaNOZZ03LNkKALX8sTmg5yiGUyE0SB"
FORGE_CLIENT_SECRET = "D07UTCz63B5YqMJW0g8xq43bd3WSre7G6zcAQ3vLenqcaNSa01GSZ19dsr1nODMX"
FORGE_BUCKET = "test-lineamientos"
FORGE_SCOPES = "data:read data:write viewables:read"

# Función para obtener el token de acceso
def get_access_token():
    url = "https://developer.api.autodesk.com/authentication/v1/authenticate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "client_id": FORGE_CLIENT_ID,
        "client_secret": FORGE_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": FORGE_SCOPES
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Error al obtener el token de acceso")

# Función para subir el archivo a Forge
def upload_file_to_forge(file_path):
    access_token = get_access_token()
    url = f"https://developer.api.autodesk.com/oss/v2/buckets/{FORGE_BUCKET}/objects"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    if not os.path.exists(file_path):
        raise Exception(f"El archivo {file_path} no existe en el sistema local")

    # Abrir el archivo y subirlo a Forge
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        return response.json()  # Devuelve la respuesta de Forge, que incluye objectId y metadata
    else:
        raise Exception("Error al subir el archivo a Forge: " + response.text)
