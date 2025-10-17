from django.shortcuts import render
from django.conf import settings
from viewer.services import (
    get_access_token,
    create_bucket_if_not_exists,
    upload_file,
    translate_file,
    list_objects_in_bucket,
    check_translation_status
)
import os, logging, base64

logger = logging.getLogger(__name__)
# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def upload_local_dwg(request):
    try:
        file_path = os.path.join(settings.BASE_DIR, "viewer", "static", "dwg_files", "ARQ_DIN_UDI.dwg")
        if not os.path.exists(file_path):
            return render(request, "error.html", {"message": "Archivo DWG no encontrado"})

        token = get_access_token()
        bucket_key = create_bucket_if_not_exists(token)
        object_name = "ARQ_DIN_UDI.dwg"

        existing_objects = list_objects_in_bucket(token, bucket_key)
        object_id = f"urn:adsk.objects:os.object:{bucket_key}/{object_name}"

        if object_name not in existing_objects:
            # Archivo no existe → subir + traducir
            object_id_raw = upload_file(token, file_path, object_name, bucket_key)
            urn = translate_file(token, object_id_raw)
            logger.debug(f"Archivo subido y traducido: {urn}")
        else:
            # Archivo ya existe, revisamos traducción
            if not check_translation_status(token, object_id):
                urn = translate_file(token, object_id)
                logger.debug(f"Archivo existente pero traducido ahora: {urn}")
            else:
                urn = base64.b64encode(object_id.encode()).decode().rstrip("=")
                logger.debug(f"Archivo ya subido y traducido: {urn}")

        return render(request, "core/home.html", {"token": token, "urn": urn})

    except Exception as e:
        logger.exception("Error subiendo o traduciendo archivo")
        return render(request, "viewer/error.html", {"message": str(e)})
