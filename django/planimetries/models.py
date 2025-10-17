from django.db import models
from core.models import BaseModel

class Planimetry(BaseModel):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    name_alt = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    
    STATUS_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('En trámite', 'En trámite'),
        ('Rechazado', 'Rechazado'),
    ]
    state = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    source = models.CharField(max_length=50)
    version = models.CharField(max_length=5)
    description = models.TextField()
    speciality = models.CharField(max_length=50)
    urn = models.CharField(max_length=255)
    
    FORMAT_CHOICES = [
        ('dwg', 'DWG'),
        ('revit', 'Revit'),
        ('otros', 'Otros'),
    ]
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.code})"
