from django.db import models
from datetime import date

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    @property
    def edad(self):
        if self.fecha_nacimiento:
            hoy = date.today()
            # Resta los años y ajusta si aún no cumple años en el año actual
            return hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return "N/A"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"