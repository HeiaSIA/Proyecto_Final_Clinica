from django.urls import path
from .views import (
    login_view, logout_view, dashboard_view,
    index_pacientes, crear_paciente, editar_paciente, eliminar_paciente,
    importar_pacientes
)

urlpatterns = [
    # Autenticación y Dashboard
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Rutas del CRUD de Pacientes
    path('pacientes/', index_pacientes, name='index_pacientes'),
    path('pacientes/crear/', crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:id>/', editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:id>/', eliminar_paciente, name='eliminar_paciente'),
    path('pacientes/importar/', importar_pacientes, name='importar_pacientes'),  # 2. Ruta agregada
]