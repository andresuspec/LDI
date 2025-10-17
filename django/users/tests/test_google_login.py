from unittest import TestCase, mock
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from users.pipeline import validate_uspec_user, create_user_with_email, sync_user_role
from users.models import ExternalUser

User = get_user_model()


class PipelineFlowTests(TestCase):
    def setUp(self):
        User.objects.all().delete()  # Limpia cualquier usuario previo
        self.details = {
            "email": "juan.perez@uspec.gov.co",
            "first_name": "Juan",
            "last_name": "Pérez"
        }
        self.strategy = mock.MagicMock()
        self.strategy.session_set = mock.MagicMock()
        self.strategy.session_get = mock.MagicMock(return_value=None)

    @mock.patch("users.pipeline.ExternalUser.objects.using")
    def test_validate_uspec_user_ok(self, mock_using):
        """
        ✅ Verifica que el pipeline acepte un email válido del dominio y lo guarde en sesión.
        """
        mock_manager = mock.Mock()
        mock_user = mock.Mock(role="interno", firstName="Juan", lastName="Pérez")
        mock_manager.get.return_value = mock_user
        mock_using.return_value = mock_manager

        validate_uspec_user(self.strategy, self.details, backend=None)

        # Validar que se haya guardado en sesión
        self.strategy.session_set.assert_called_once()
        args, kwargs = self.strategy.session_set.call_args
        key, data = args
        assert key == "external_data"
        assert data["role"] == "interno"

    def test_validate_uspec_user_domain_invalid(self):
        """
        ❌ Debe fallar si el dominio no es uspec.gov.co
        """
        details = {"email": "juan@gmail.com"}
        with self.assertRaises(PermissionDenied):
            validate_uspec_user(self.strategy, details, backend=None)

    def test_create_user_with_email_creates_user(self):
        """
        ✅ Crea un usuario local con base en el email si no existe.
        """
        result = create_user_with_email(self.strategy, self.details, backend=None)
        user = result["user"]
        self.assertTrue(User.objects.filter(email=self.details["email"]).exists())
        self.assertEqual(user.username, "juan.perez")

    def test_sync_user_role_updates_fields(self):
        """
        ✅ Sincroniza datos externos con el usuario existente.
        """
        user = User.objects.create_user(
            username="juan.perez",
            email="juan.perez@uspec.gov.co",
            first_name="J",
            last_name="P"
        )

        # Datos externos simulados
        external_data = {
            "role": "interno",
            "first_name": "Juan",
            "last_name": "Pérez"
        }
        self.strategy.session_get.return_value = external_data

        sync_user_role(self.strategy, self.details, user=user)
        user.refresh_from_db()

        self.assertEqual(user.role, "interno")
        self.assertEqual(user.first_name, "Juan")
        self.assertEqual(user.last_name, "Pérez")
