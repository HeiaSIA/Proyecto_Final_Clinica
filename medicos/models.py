from django.db import models

class Medico(models.Model):
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")
    registro_profesional = models.CharField(max_length=50, unique=True, verbose_name="Registro Profesional")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    
    activo = models.BooleanField(
        default=True, 
        verbose_name="Estado Activo",
        help_text="Desmárcalo para suspender al médico y bloquear nuevas citas."
    )

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ['-activo', 'apellidos'] # Ordena primero por activos, luego alfabéticamente

    def __str__(self):
        return f"Dr(a). {self.nombres} {self.apellidos} - {self.especialidad}"