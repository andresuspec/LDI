from django.db import models

class ExternalUser(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=150)
    firstName = models.CharField(max_length=150)
    lastName = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "employees"
        app_label = "users"
