from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cita
from medicos.models import Medico
from pacientes.models import Paciente

def index_citas(request):
    citas = Cita.objects.select_related('paciente', 'medico').all().order_by('-fecha', '-hora')
    return render(request, 'index_citas.html', {'citas': citas})

def crear_cita(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        medico_id = request.POST.get('medico')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        motivo = request.POST.get('motivo')

        paciente = Paciente.objects.get(id=paciente_id)
        medico = Medico.objects.get(id=medico_id)

        Cita.objects.create(
            paciente=paciente,
            medico=medico,
            fecha=fecha,
            hora=hora,
            motivo=motivo,
            estado='PENDIENTE'
        )
        messages.success(request, '¡Cita médica agendada exitosamente!')
        return redirect('index_citas')

    pacientes = Paciente.objects.all()
    medicos_activos = Medico.objects.filter(activo=True)
    return render(request, 'crear_cita.html', {
        'pacientes': pacientes,
        'medicos': medicos_activos
    })

def editar_cita(request, id):
    cita = Cita.objects.get(id=id)
    
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        medico_id = request.POST.get('medico')
        
        cita.paciente = Paciente.objects.get(id=paciente_id)
        cita.medico = Medico.objects.get(id=medico_id)
        cita.fecha = request.POST.get('fecha')
        cita.hora = request.POST.get('hora')
        cita.estado = request.POST.get('estado')
        cita.motivo = request.POST.get('motivo')
        
        cita.save()
        messages.success(request, '¡Cita actualizada correctamente!')
        return redirect('index_citas')

    pacientes = Paciente.objects.all()
    medicos = Medico.objects.filter(activo=True)
    return render(request, 'editar_cita.html', {
        'cita': cita,
        'pacientes': pacientes,
        'medicos': medicos
    })

def eliminar_cita(request, id):
    cita = Cita.objects.get(id=id)
    cita.delete()
    messages.success(request, 'La cita ha sido eliminada del registro.')
    return redirect('index_citas')