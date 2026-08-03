from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Paciente
import pandas as pd
from .forms import CSVForm

# ==========================================
# AUTENTICACIÓN Y DASHBOARD
# ==========================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('user')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.username}!')
            return redirect('dashboard') 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


# ==========================================
# CRUD DE PACIENTES
# ==========================================

@login_required
def index_pacientes(request):
    query = request.GET.get('buscar', '')
    
    if query:
        pacientes = Paciente.objects.filter(cedula__icontains=query)
    else:
        pacientes = Paciente.objects.all()
        
    return render(request, 'pacientes/index_pacientes.html', {'pacientes': pacientes, 'query': query})

@login_required
def crear_paciente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        
        Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            fecha_nacimiento=fecha_nacimiento,
            telefono=telefono,
            direccion=direccion
        )
        messages.success(request, 'Paciente registrado exitosamente.')
        return redirect('index_pacientes')

    return render(request, 'pacientes/crear_paciente.html')

@login_required
def editar_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    
    if request.method == 'POST':
        paciente.nombre = request.POST.get('nombre')
        paciente.apellido = request.POST.get('apellido')
        paciente.cedula = request.POST.get('cedula')
        fecha_n = request.POST.get('fecha_nacimiento')
        if fecha_n:
            paciente.fecha_nacimiento = fecha_n
        paciente.telefono = request.POST.get('telefono')
        paciente.direccion = request.POST.get('direccion')
        
        paciente.save()
        messages.warning(request, 'Datos del paciente actualizados exitosamente.')
        return redirect('index_pacientes')
    
    fecha_str = paciente.fecha_nacimiento.strftime('%Y-%m-%d') if paciente.fecha_nacimiento else ''
    
    return render(request, 'pacientes/editar_paciente.html', {
        'paciente': paciente, 
        'fecha_str': fecha_str
    })

@login_required
def eliminar_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    paciente.delete()
    messages.info(request, 'Paciente eliminado.')
    return redirect('index_pacientes')

@login_required
def importar_pacientes(request):
    if request.method == 'POST':

        
        messages.success(request, 'Pacientes importados correctamente.')
        return redirect('index_pacientes')
        
    return render(request, 'pacientes/importar_pacientes.html')

@login_required
def importar_pacientes(request):
    if request.method == 'POST':
        formulario = CSVForm(request.POST, request.FILES)
        if formulario.is_valid():
            archivo = request.FILES['archivo']
            
            try:
                # Leemos el archivo CSV
                df = pd.read_csv(archivo)
                
                # Rellenamos los valores vacíos (NaN) con un string vacío para evitar errores en base de datos
                df = df.fillna('')
                
                for _, fila in df.iterrows():
                    Paciente.objects.create(
                        nombre = fila['nombre'],
                        apellido = fila['apellido'],
                        cedula = fila['cedula'],
                        # Si la fecha está vacía, guardamos None para no romper el formato de fecha de Django
                        fecha_nacimiento = fila['fecha_nacimiento'] if fila['fecha_nacimiento'] else None,
                        telefono = fila['telefono'],
                        direccion = fila['direccion'],
                    )
                messages.success(request, "Pacientes importados con éxito")
                return redirect('index_pacientes')
            
            except Exception as e:
                messages.error(request, f"Error al leer el archivo: Asegúrate de que las columnas sean correctas.")
        else:
            messages.error(request, "Error al importar pacientes")
    else:
        formulario = CSVForm()

    return render(request, 'pacientes/importar_pacientes.html', {'formulario': formulario})