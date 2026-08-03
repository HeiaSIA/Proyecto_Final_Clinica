from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Factura, DetalleFactura
from pacientes.models import Paciente
from medicamentos.models import Medicamento


def index_facturas(request):
    facturas = Factura.objects.select_related('paciente').all().order_by('-pk')
    return render(request, 'index_facturas.html', {'facturas': facturas})


def crear_factura(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        concepto = request.POST.get('concepto')

        # 1. Validaciones preventivas de datos de entrada
        if not paciente_id:
            messages.error(request, 'Debe seleccionar un paciente válido.')
            return redirect('crear_factura')

        try:
            precio_consulta = float(request.POST.get('precio_consulta', 0) or 0)
        except ValueError:
            messages.error(request, 'El costo de la consulta debe ser un número válido.')
            return redirect('crear_factura')

        # Usamos pk para soportar cualquier nombre de Primary Key en el modelo
        try:
            paciente = Paciente.objects.get(pk=paciente_id)
        except Paciente.DoesNotExist:
            messages.error(request, 'El paciente seleccionado no existe.')
            return redirect('crear_factura')

        # 2. Bloque Atómico: Todo se guarda junto o nada cambia en la base de datos
        try:
            with transaction.atomic():
                # Crear cabecera de factura
                factura = Factura.objects.create(
                    paciente=paciente,
                    concepto=concepto,
                    subtotal=precio_consulta
                )

                medicamento_ids = request.POST.getlist('medicamento_id[]')
                cantidades = request.POST.getlist('cantidad[]')
                subtotal_medicamentos = 0.0

                for m_id, cant in zip(medicamento_ids, cantidades):
                    if m_id and cant and int(cant) > 0:
                        cant_num = int(cant)
                        medicamento = Medicamento.objects.get(pk=m_id)

                        # Validación backend de stock antes de descontar
                        if medicamento.stock < cant_num:
                            raise ValueError(f'Stock insuficiente para: {medicamento.nombre}')

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

                # Totales finales (Subtotal + IVA 15%)
                subtotal_acumulado = precio_consulta + subtotal_medicamentos
                iva_calculado = round(subtotal_acumulado * 0.15, 2)
                total_calculado = round(subtotal_acumulado + iva_calculado, 2)

                factura.subtotal = round(subtotal_acumulado, 2)
                factura.iva = iva_calculado
                factura.total = total_calculado
                factura.save()

                messages.success(request, 'Factura generada y stock descontado correctamente.')
                return redirect('index_facturas')

        except ValueError as ve:
            messages.error(request, str(ve))
            return redirect('crear_factura')
        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado al procesar la factura: {e}')
            return redirect('crear_factura')

    # GET: Cargar formulario
    pacientes = Paciente.objects.filter(citas__isnull=False).distinct()
    medicamentos = Medicamento.objects.all()
    return render(request, 'crear_factura.html', {
        'pacientes': pacientes,
        'medicamentos': medicamentos
    })


def ver_factura(request, id):
    factura = get_object_or_404(Factura, pk=id)
    detalles = factura.detalles.all()
    return render(request, 'ver_factura.html', {
        'factura': factura,
        'detalles': detalles
    })


def editar_factura(request, id):
    factura = get_object_or_404(Factura, pk=id)

    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')

        if not paciente_id:
            messages.error(request, 'Debe seleccionar un paciente válido.')
            return redirect('editar_factura', id=id)

        try:
            factura.paciente = Paciente.objects.get(pk=paciente_id)
            factura.concepto = request.POST.get('concepto')

            subtotal = float(request.POST.get('subtotal', 0) or 0)
            factura.subtotal = subtotal
            factura.iva = round(subtotal * 0.15, 2)
            factura.total = round(subtotal + factura.iva, 2)
            factura.save()

            messages.success(request, 'Factura actualizada correctamente.')
            return redirect('index_facturas')
        except Exception as e:
            messages.error(request, f'Error al editar la factura: {e}')

    pacientes = Paciente.objects.filter(citas__isnull=False).distinct()
    return render(request, 'editar_factura.html', {
        'factura': factura,
        'pacientes': pacientes
    })


def eliminar_factura(request, id):
    factura = get_object_or_404(Factura, pk=id)
    factura.delete()
    messages.success(request, 'Factura eliminada de la base de datos.')
    return redirect('index_facturas')