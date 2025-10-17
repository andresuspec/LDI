import logging
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from users.models import User, ExternalUser

logger = logging.getLogger(__name__)
User = get_user_model()


def create_user_with_email(strategy, details, backend, user=None, *args, **kwargs):
    """
    Crea un usuario nuevo con el email como username si no existe.
    """
    if user:
        return {"user": user}

    email = details.get("email")
    if not email:
        return None

    username = email.split("@")[0]
    user = User.objects.create_user(
        username=username,
        email=email,
    )
    return {"user": user}


def validate_uspec_user(strategy, details, backend, **kwargs):
    """
    Verifica dominio y obtiene datos de la BD externa (especaps).
    """
    email = details.get("email")

    if not email or not email.endswith("@uspec.gov.co"):
        raise PermissionDenied("Solo se permiten cuentas del dominio uspec.gov.co")

    external_data = {}
    try:
        external_user = ExternalUser.objects.using("especaps").get(email=email)
        external_data = {
            "role": getattr(external_user, "role", None),
            "first_name": getattr(external_user, "firstName", None),
            "last_name": getattr(external_user, "lastName", None),
        }
        logger.debug(f"🟦 Usuario externo encontrado: {external_data}")
    except ExternalUser.DoesNotExist:
        raise PermissionDenied("No estás autorizado para acceder con Google")

    # Combinar con los datos de Google si faltan
    external_data["first_name"] = external_data.get("first_name") or details.get("first_name")
    external_data["last_name"] = external_data.get("last_name") or details.get("last_name")

    # Guardar en sesión para usar en sync_user_role
    strategy.session_set("external_data", external_data)


def sync_user_role(strategy, details, user=None, **kwargs):
    """
    Sincroniza el usuario local con los datos externos y de Google.
    """
    if not user:
        return

    external_data = strategy.session_get("external_data")
    if not external_data:
        logger.debug("⚠️ No hay datos externos en sesión, se omite sincronización.")
        return

    role = external_data.get("role")
    first_name = external_data.get("first_name")
    last_name = external_data.get("last_name")

    updated = False

    if role and getattr(user, "role", None) != role:
        user.role = role
        updated = True

    if first_name and user.first_name != first_name:
        user.first_name = first_name
        updated = True

    if last_name and user.last_name != last_name:
        user.last_name = last_name
        updated = True

    if updated:
        user.save()
        logger.debug(f"✅ Usuario sincronizado: {user.email} ({first_name} {last_name})")
