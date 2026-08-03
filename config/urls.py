from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pacientes.urls')),  
    path('medicos/', include('medicos.urls')),  
    path('citas/', include('citas.urls')),  
    path('medicamentos/', include('medicamentos.urls')),  
    path('facturacion/', include('facturacion.urls')),  
    path('predicciones/', include('predicciones.urls')),  
]