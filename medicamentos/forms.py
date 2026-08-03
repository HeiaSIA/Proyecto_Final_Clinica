from django import forms

class CSVMedicamentoForm(forms.Form):
    archivo = forms.FileField(
        label='Selecciona un archivo CSV o Excel',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv, .xls, .xlsx'})
    )