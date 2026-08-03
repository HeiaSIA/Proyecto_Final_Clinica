from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_medicamentos, name='index_medicamentos'),
    path('crear/', views.crear_medicamento, name='crear_medicamento'),
    path('editar/<int:id>/', views.editar_medicamento, name='editar_medicamento'),
    path('eliminar/<int:id>/', views.eliminar_medicamento, name='eliminar_medicamento'),
    path('medicamentos/importar/', views.importar_medicamentos, name='importar_medicamentos'),
]