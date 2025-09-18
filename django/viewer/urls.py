# viewer/urls.py
from django.urls import path
from . import views

urlpatterns = [
     path("upload-local-dwg/", views.upload_local_dwg, name="upload_local_dwg"),
]
