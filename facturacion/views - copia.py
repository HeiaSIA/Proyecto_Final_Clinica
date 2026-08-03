from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Factura, DetalleFactura
from pacientes.models import Paciente
from medicamentos.models import Medicamento

def index_facturas(request):
    facturas = Factura.objects.all().order_by('-id')
    return render(request, 'index_facturas.html', {'facturas': facturas})

def crear_factura(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        concepto = request.POST.get('concepto')
        precio_consulta = float(request.POST.get('precio_consulta', 0))

        paciente = Paciente.objects.get(id=paciente_id)

        # 1. Crear cabecera
        factura = Factura.objects.create(
            paciente=paciente,
            concepto=concepto,
            subtotal=precio_consulta
        )

        # 2. Agregar medicamentos y descontar stock
        medicamento_ids = request.POST.getlist('medicamento_id[]')
        cantidades = request.POST.getlist('cantidad[]')

        subtotal_medicamentos = 0.0

        for m_id, cant in zip(medicamento_ids, cantidades):
            if m_id and cant and int(cant) > 0:
                medicamento = Medicamento.objects.get(id=m_id)
                cant_num = int(cant)

                # Descontar del inventario
                medicamento.stock -= cant_num
                medicamento.save()

                sub_item = float(medicamento.precio_unitario) * cant_num
                subtotal_medicamentos += sub_item

                DetalleFactura.objects.create(
                    factura=factura,
                    medicamento=medicamento,
                    cantidad=cant_num,
                    precio_unitario=medicamento.precio_unitario,
                    subtotal=sub_item
                )

        # 3. Totales finales
        subtotal_acumulado = precio_consulta + subtotal_medicamentos
        iva_calculado = round(subtotal_acumulado * 0.15, 2)
        total_calculado = round(subtotal_acumulado + iva_calculado, 2)

        factura.subtotal = round(subtotal_acumulado, 2)
        factura.iva = iva_calculado
        factura.total = total_calculado
        factura.save()

        messages.success(request, 'Factura generada y stock descontado correctamente.')
        return redirect('index_facturas')

    pacientes = Paciente.objects.all()
    medicamentos = Medicamento.objects.all()
    return render(request, 'crear_factura.html', {
        'pacientes': pacientes,
        'medicamentos': medicamentos
    })

def ver_factura(request, id):
    factura = Factura.objects.get(id=id)
    detalles = factura.detalles.all()
    return render(request, 'ver_factura.html', {
        'factura': factura,
        'detalles': detalles
    })

def editar_factura(request, id):
    factura = Factura.objects.get(id=id)
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        factura.paciente = Paciente.objects.get(id=paciente_id)
        factura.concepto = request.POST.get('concepto')
        
        subtotal = float(request.POST.get('subtotal', 0))
        factura.subtotal = subtotal
        factura.iva = round(subtotal * 0.15, 2)
        factura.total = round(subtotal + factura.iva, 2)
        factura.save()

        messages.success(request, 'Factura actualizada correctamente.')
        return redirect('index_facturas')

    pacientes = Paciente.objects.all()
    return render(request, 'editar_factura.html', {
        'factura': factura,
        'pacientes': pacientes
    })

def eliminar_factura(request, id):
    factura = Factura.objects.get(id=id)
    factura.delete()  # Borrado físico directo de BD
    messages.success(request, 'Factura eliminada de la base de datos.')
    return redirect('index_facturas')