from django.urls import path, include
from users.views.auth import login_view
from django.views.generic import TemplateView
app_name = "users"

urlpatterns = [
    path('login/', login_view, name='login'),
    path(
        "login-error/",
        TemplateView.as_view(template_name="users/login_error.html"),
        name="login_error"
    ),
]
