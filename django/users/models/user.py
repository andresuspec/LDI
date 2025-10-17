from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Administrador"),
        ("interno", "Usuario interno"),
        ("externo", "Usuario externo"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="externo")
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
