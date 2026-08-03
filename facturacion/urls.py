from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_facturas, name='index_facturas'),
    path('crear/', views.crear_factura, name='crear_factura'),
    path('ver/<int:id>/', views.ver_factura, name='ver_factura'),
    path('editar/<int:id>/', views.editar_factura, name='editar_factura'),
    path('eliminar/<int:id>/', views.eliminar_factura, name='eliminar_factura'),
]