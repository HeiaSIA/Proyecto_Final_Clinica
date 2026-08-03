from django import forms
from .models import Factura
from pacientes.models import Paciente

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['paciente', 'concepto', 'costo_consulta'] # Ajusta con los nombres reales de tu modelo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 🔹 Filtra solo pacientes que tengan al menos 1 cita asociada
        # .distinct() evita que un paciente con varias citas salga duplicado en la lista
        self.fields['paciente'].queryset = Paciente.objects.filter(
            citas__isnull=False
        ).distinct()

        # 🔹 (Opcional) Define cómo quieres que se muestre en el select
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido} - Cédula: {obj.cedula}"