from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Medicamento
import pandas as pd
from .forms import CSVMedicamentoForm

def index_medicamentos(request):
    medicamentos = Medicamento.objects.all().order_by('-id')
    return render(request, 'index_medicamentos.html', {'medicamentos': medicamentos})

def crear_medicamento(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        lote = request.POST.get('lote')
        stock = request.POST.get('stock')
        precio_unitario = request.POST.get('precio_unitario')

        Medicamento.objects.create(
            nombre=nombre,
            lote=lote,
            stock=stock,
            precio_unitario=precio_unitario
        )
        messages.success(request, 'Medicamento registrado correctamente en el inventario.')
        return redirect('index_medicamentos')

    return render(request, 'crear_medicamento.html')

def editar_medicamento(request, id):
    medicamento = Medicamento.objects.get(id=id)
    if request.method == 'POST':
        medicamento.nombre = request.POST.get('nombre')
        medicamento.lote = request.POST.get('lote')
        medicamento.stock = request.POST.get('stock')
        medicamento.precio_unitario = request.POST.get('precio_unitario')
        medicamento.save()

        messages.success(request, 'Medicamento actualizado correctamente.')
        return redirect('index_medicamentos')

    return render(request, 'editar_medicamento.html', {'medicamento': medicamento})

def eliminar_medicamento(request, id):
    medicamento = Medicamento.objects.get(id=id)
    medicamento.delete()
    messages.success(request, 'Medicamento eliminado permanentemente de la base de datos.')
    return redirect('index_medicamentos')


def importar_medicamentos(request):
    if request.method == 'POST':
        formulario = CSVMedicamentoForm(request.POST, request.FILES)
        if formulario.is_valid():
            archivo = request.FILES['archivo']
            try:
                # Leer dependiendo de la extensión
                if archivo.name.endswith('.csv'):
                    df = pd.read_csv(archivo)
                else:
                    df = pd.read_excel(archivo)
                
                # Iterar y crear los medicamentos
                for _, row in df.iterrows():
                    Medicamento.objects.create(
                        nombre=row['nombre'],
                        lote=row['lote'],
                        stock=row['stock'],
                        precio_unitario=row['precio_unitario']
                    )
                
                messages.success(request, '¡Inventario de medicamentos importado con éxito!')
                return redirect('index_medicamentos')
            
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
                return redirect('importar_medicamentos')
    else:
        formulario = CSVMedicamentoForm()

    return render(request, 'importar_medicamentos.html', {'formulario': formulario})