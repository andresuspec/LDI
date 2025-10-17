from django.db import models
from core.models import BaseModel
from planimetries.models import Planimetry
from zones.models import Zone

class Building(BaseModel):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="buildings")
    planimetry = models.ForeignKey(Planimetry, on_delete=models.CASCADE, related_name="buildings")

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    usage = models.CharField(max_length=20)
    ind_desc = models.CharField(max_length=20)
    indicator = models.CharField(max_length=20)
    min_usable_area = models.CharField(max_length=20)
    coefficient_security = models.CharField(max_length=20)
    data_source = models.CharField(max_length=20)
    generalities = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.code})"
