from django.shortcuts import render
from django.contrib import messages
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
from citas.models import Cita 
from medicamentos.models import Medicamento

def prediccion_citas(request):
    # 1. Traemos los nombres correctos de los campos del modelo
    citas = Cita.objects.all().values('medico__especialidad', 'fecha')
    df = pd.DataFrame(citas)
    
    if df.empty:
        messages.error(request, 'No hay citas registradas para analizar.')
        return render(request, 'predicciones/citas.html', {'predicciones': []})

    # 2. Renombramos la columna para que el resto de tu código funcione igual
    df.rename(columns={'medico__especialidad': 'especialidad'}, inplace=True)

    # 3. Procesamiento de fechas usando la columna real 'fecha'
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['mes'] = df['fecha'].dt.month
    df['anio'] = df['fecha'].dt.year
    df['periodo'] = df['anio'] * 12 + df['mes']

    # Agrupamos por especialidad y contamos
    resumen = df.groupby(['especialidad', 'periodo']).size().reset_index(name='cantidad_citas')

    predicciones = []
    especialidades = resumen['especialidad'].unique()

    for especialidad in especialidades:
        datos = resumen[resumen['especialidad'] == especialidad].sort_values('periodo')
        
        if len(datos) < 2:
            continue

        x = datos[['periodo']]
        y = datos['cantidad_citas']
        
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        
        modelo = LinearRegression()
        modelo.fit(x_train, y_train)
        
        ultimo_periodo = datos['periodo'].max()
        proximo_periodo = ultimo_periodo + 1
        prediccion_val = modelo.predict(pd.DataFrame({'periodo': [proximo_periodo]}))[0]

        predicciones.append({
            'especialidad': especialidad,
            'citas_actuales': int(y.iloc[-1]),
            'prediccion_proximo_mes': round(float(prediccion_val))
        })

    return render(request, 'predicciones/citas.html', {'predicciones': predicciones})


def prediccion_medicamentos(request):
    # 1. Usamos los campos que SÍ existen en tu modelo: 'stock' y 'creado_en'
    medicamentos = Medicamento.objects.all().values('nombre', 'stock', 'creado_en')
    df = pd.DataFrame(medicamentos)
    
    if df.empty:
        messages.error(request, 'No hay registro de medicamentos.')
        return render(request, 'predicciones/medicamentos.html', {'predicciones': []})

    # 2. Procesamiento usando 'creado_en'
    df['creado_en'] = pd.to_datetime(df['creado_en'])
    df['mes'] = df['creado_en'].dt.month
    df['anio'] = df['creado_en'].dt.year
    df['periodo'] = df['anio'] * 12 + df['mes']

    # 3. Agrupamos por nombre de medicamento y SUMAMOS el 'stock'
    resumen = df.groupby(['nombre', 'periodo'])['stock'].sum().reset_index()

    predicciones = []
    nombres_med = resumen['nombre'].unique()

    for nombre in nombres_med:
        datos = resumen[resumen['nombre'] == nombre].sort_values('periodo')
        
        if len(datos) < 2:
            continue

        x = datos[['periodo']]
        y = datos['stock']  # Cambiado a 'stock'
        
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        
        modelo = LinearRegression()
        modelo.fit(x_train, y_train)
        
        ultimo_periodo = datos['periodo'].max()
        proximo_periodo = ultimo_periodo + 1
        prediccion_val = modelo.predict(pd.DataFrame({'periodo': [proximo_periodo]}))[0]

        predicciones.append({
            'medicamento': nombre,
            'consumo_actual': int(y.iloc[-1]),
            'prediccion_demanda': round(float(prediccion_val))
        })

    return render(request, 'predicciones/medicamentos.html', {'predicciones': predicciones})