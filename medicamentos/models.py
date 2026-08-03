from django.db import models

class Medicamento(models.Model):
    nombre = models.CharField(max_length=150)
    lote = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} (Lote: {self.lote})"

    @property
    def es_stock_bajo(self):
        return self.stock < 5