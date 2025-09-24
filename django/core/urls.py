from django.urls import path
from . import views


urlpatterns = [
    path('', views.upload_local_dwg, name='home'),
]
