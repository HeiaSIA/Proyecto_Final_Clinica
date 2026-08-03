from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_citas, name='index_citas'),
    path('crear/', views.crear_cita, name='crear_cita'),
    path('editar/<int:id>/', views.editar_cita, name='editar_cita'),
    path('eliminar/<int:id>/', views.eliminar_cita, name='eliminar_cita'),
]