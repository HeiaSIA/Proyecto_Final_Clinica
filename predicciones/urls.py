# predicciones/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('flujo-citas/', views.prediccion_citas, name='prediccion_citas'),
]