from django.db import models
from core.models import BaseModel
from templates_project.models import ProjectTemplateType
from planimetries.models import Planimetry

class Zone(BaseModel):
    id = models.CharField(max_length=50, primary_key=True)
    proyect_type = models.ForeignKey(ProjectTemplateType, on_delete=models.CASCADE, related_name="zones")
    planimetry = models.ForeignKey(Planimetry, on_delete=models.CASCADE, related_name="zones")
    nomenclature = models.CharField(max_length=50)
    buildings_amount = models.PositiveIntegerField()

    def __str__(self):
        return f"Zona {self.nomenclature} ({self.buildings_amount} edificios)"
