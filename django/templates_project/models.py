from django.db import models
from core.models import BaseModel

class ProjectTemplateType(BaseModel):
    code = models.CharField(max_length=10, unique=True)
    planimetry_id = models.CharField(max_length=100)
    project_name = models.TextField()
    description = models.TextField()
    capacity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.code} - {self.project_name}"
