from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

EXEMPT_URLS = [
    '/login/',
    '/register/',
    '/admin/',
    '/static/',
    '/media/',
    '/auth/',
    '/users/login-error/',
]

class LoginRequiredMiddleware:
    """
    Middleware que redirige a /login si el usuario no está autenticado,
    excepto para las URLs exentas.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_path = request.path

        # Permitir acceso a las URLs exentas
        if any(current_path.startswith(url) for url in EXEMPT_URLS):
            return self.get_response(request)

        # Redirigir si no está autenticado
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)
