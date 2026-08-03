from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Medico

def index_doctores(request):
    doctores = Medico.objects.all()
    return render(request, 'index_doctores.html', {'doctores': doctores})

def crear_doctor(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        especialidad = request.POST.get('especialidad')
        registro_profesional = request.POST.get('registro_profesional')
        telefono = request.POST.get('telefono')
        activo = request.POST.get('activo') == 'on'

        Medico.objects.create(
            nombres=nombres,
            apellidos=apellidos,
            especialidad=especialidad,
            registro_profesional=registro_profesional,
            telefono=telefono,
            activo=activo
        )
        messages.success(request, '¡Médico registrado correctamente!')
        return redirect('index_doctores')
    
    return render(request, 'crear_doctor.html')

def editar_doctor(request, id):
    doctor = Medico.objects.get(id=id)
    
    if request.method == 'POST':
        doctor.nombres = request.POST.get('nombres')
        doctor.apellidos = request.POST.get('apellidos')
        doctor.especialidad = request.POST.get('especialidad')
        doctor.registro_profesional = request.POST.get('registro_profesional')
        doctor.telefono = request.POST.get('telefono')
        doctor.activo = request.POST.get('activo') == 'on'
        
        doctor.save()
        messages.success(request, '¡Datos del médico actualizados correctamente!')
        return redirect('index_doctores')
    
    return render(request, 'editar_doctor.html', {'doctor': doctor})

def eliminar_doctor(request, id):
    doctor = Medico.objects.get(id=id)
    doctor.delete()
    messages.success(request, 'El médico ha sido eliminado del sistema.')
    return redirect('index_doctores')