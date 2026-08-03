from django.db import models
from pacientes.models import Paciente
from medicamentos.models import Medicamento

class Factura(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='facturas')
    concepto = models.CharField(max_length=200)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Factura #{self.pk} - {self.paciente.nombre} {self.paciente.apellido}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.medicamento.nombre} (Factura #{self.factura.id})"