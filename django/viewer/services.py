import base64
import requests
from django.conf import settings
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

AUTH_URL = "https://developer.api.autodesk.com/authentication/v2/token"
OSS_URL = "https://developer.api.autodesk.com/oss/v2/buckets"
DERIVATIVE_URL = "https://developer.api.autodesk.com/modelderivative/v2/designdata"

def get_access_token():
    data = {
        "client_id": settings.FORGE_CLIENT_ID,
        "client_secret": settings.FORGE_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "data:read data:write data:create bucket:read bucket:create bucket:delete"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(AUTH_URL, data=data, headers=headers)
    r.raise_for_status()
    token = r.json()["access_token"]
    logger.debug("DEBUG >>> token obtenido: %s", token)
    return token

def create_bucket_if_not_exists(token):
    bucket_key = settings.FORGE_BUCKET_KEY.lower()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "x-ads-region": "US"}
    data = {"bucketKey": bucket_key, "policyKey": "persistent"}
    r = requests.post(OSS_URL, headers=headers, json=data)
    if r.status_code == 409:  # ya existe
        logger.debug("DEBUG >>> Bucket ya existía: %s", bucket_key)
    elif r.status_code == 200:
        logger.debug("DEBUG >>> Bucket creado: %s", bucket_key)
    else:
        r.raise_for_status()
    return bucket_key

def upload_file(token, file_path, object_name, bucket_key):
    # 1. Obtener pre-signed URL
    headers = {"Authorization": f"Bearer {token}", "x-ads-region": "US"}
    url = f"{OSS_URL}/{bucket_key}/objects/{object_name}/signeds3upload"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    signed_data = r.json()

    # 2. Subir archivo a S3
    s3_url = signed_data["urls"][0]
    with open(file_path, "rb") as f:
        r2 = requests.put(s3_url, data=f)
        r2.raise_for_status()
    logger.debug("DEBUG >>> Archivo subido a S3")

    # 3. Confirmar upload
    upload_key = signed_data.get("uploadKey")
    etag = r2.headers.get("ETag", "").replace('"','')
    body = {"uploadKey": upload_key, "parts": [{"partNumber": 1, "etag": etag}]}
    r3 = requests.post(url, headers=headers, json=body)
    r3.raise_for_status()
    object_id = r3.json().get("objectId")
    if not object_id:
        # fallback a URN de bucket/object
        object_id = f"urn:adsk.objects:os.object:{bucket_key}/{object_name}"
    logger.debug("DEBUG >>> objectId final: %s", object_id)
    return object_id

def translate_file(token, object_id):
    if not isinstance(object_id, str):
        raise TypeError("object_id debe ser una cadena")
    urn = base64.b64encode(object_id.encode()).decode().rstrip("=")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    job_data = {"input": {"urn": urn}, "output": {"formats": [{"type": "svf", "views": ["2d", "3d"]}]}}
    r = requests.post(f"{DERIVATIVE_URL}/job", headers=headers, json=job_data)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error("Error MD API (403/Forbidden). Revisa token, scopes y bucket ownership: %s", e)
        raise
    logger.debug("DEBUG >>> Traducción solicitada correctamente")
    return urn

def list_objects_in_bucket(token, bucket_key):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{OSS_URL}/{bucket_key}/objects"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    objects = r.json().get("items", [])
    return [obj["objectKey"] for obj in objects]

def check_translation_status(token, object_id):
    headers = {"Authorization": f"Bearer {token}"}
    urn_base64 = base64.b64encode(object_id.encode()).decode().rstrip("=")
    r = requests.get(f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn_base64}/manifest", headers=headers)
    if r.status_code == 200:
        manifest = r.json()
        return manifest.get("status") == "success"
    return False