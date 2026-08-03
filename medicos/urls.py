from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_doctores, name='index_doctores'),
    path('crear/', views.crear_doctor, name='crear_doctor'),
    path('editar/<int:id>/', views.editar_doctor, name='editar_doctor'),
    path('eliminar/<int:id>/', views.eliminar_doctor, name='eliminar_doctor'),
]