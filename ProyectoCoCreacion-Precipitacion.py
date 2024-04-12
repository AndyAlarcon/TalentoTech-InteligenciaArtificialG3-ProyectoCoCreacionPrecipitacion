
from sodapy import Socrata
import datetime
from dateutil.relativedelta import relativedelta    
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

#Identificador interno del conjunto de datos.
datasetId = "s54a-sgyg"

cliente=Socrata('www.datos.gov.co', None)

#Se incrementa el tiempo de espera
cliente.timeout = 120

#Se realiza un conteo de la totalidad de registros del conjunto
totalRegistros = cliente.get(datasetId, select="COUNT(*)")[0]["COUNT"]

#Se define el parámetro de fecha a filtrar, como un año atrás de la fecha del sistema.
# limiteInferior = (datetime.datetime.now() - datetime.timedelta(days=365)).date()

#Aquí utilizando la librería dateutil.relativedelta, ahora se filtra por meses
limiteInferior = (datetime.datetime.now() - relativedelta(months=12)).date()

#Se define el valor del departamento a filtrar.
Departamento = "BOYACÁ"

#Se construye el filtro para la petición al API
consulta = f"departamento = '{Departamento}' AND fechaobservacion >= '{limiteInferior}' AND valorobservado <> 0"

if(int(totalRegistros) > 1000000):
    print("Inicio recuperación de datos" + str(datetime.datetime.now()))
    result=cliente.get(datasetId, where=consulta, limit=1000000)
    print("Fin recuperación de datos" + str(datetime.datetime.now()))
else:
    print("Inicio recuperación de datos" + str(datetime.datetime.now()))
    result=cliente.get(datasetId, where=consulta, limit=totalRegistros)
    print("Fin recuperación de datos" + str(datetime.datetime.now()))

## Preprocesamiento de datos con Pandas

# Convierte los resultados a DataFrame
df = pd.DataFrame.from_records(result)

print(df.head())

#Se asegura que los valores de la columna fechaobservacion, sean valores datetime
df['fechaobservacion'] = pd.to_datetime(df['fechaobservacion'])

#Se extraen los valores únicos de la columna municipios
municipios = df['municipio'].unique()
print(municipios)

# valores = df['valorobservado'].unique()
# print(valores)

#Se realiza una verificación de los datos antes de aplicar una limpieza de registros con datos nulos
df.info()
df = df.dropna(axis=0,how='any')
df.info()


# Preparación de datos para gráfico de barras
var=list((df['valorobservado']))
valores=[]
for i in range(len(var)):
  valores.append(float(var[i]))

valores_a=np.array(valores)

## Descriptivas básicas
#Media
print('El valor medio de precipitación en mm para el departamento de Boyacá en los últimos 12 meses es: ', round(np.mean(valores_a),3))
#Mediana
print('Para la precipitación en mm tomada en el departamento de Boyacá en los últimos 12 meses, el valor que se ubica justo en el medio es: ', round(np.median(valores_a),3))
#Desviación estándar
print('Para la precipitación en mm tomada en el departamento de Boyacá en los últimos 12 meses, la variación de los datos respecto al valor medio es : ', round(np.std(valores_a),3))
#Valor máximo
print('Para la precipitación en mm tomada en el departamento de Boyacá en los últimos 12 meses, el valor máximo observado es: ',round(np.max(valores_a),3))
#Valor mínimo
print('Para la precipitación en mm tomada en el departamento de Boyacá en los últimos 12 meses, el valor mínimo observado es: ',round(np.min(valores_a),3))
#Rango
print('Para la precipitación en mm tomada en el departamento de Boyacá en los últimos 12 meses, la diferencia entre el valor máximo y el valor mínimo observado es: ',round(np.max(valores_a),3)-round(np.min(valores_a),3))


var=list((df['municipio']))
municipios=[]
for i in range(len(var)):
  municipios.append(str(var[i]))

  #total de precipitación
total_precipitación = sum(valores_a)

#Grafica del histograma de precipitación por municipio
plt.bar(municipios, valores_a)

plt.text(0.5, 1.05 * max(valores_a),f'Total precipitación en Boyacá: {total_precipitación}',ha='center', fontsize=12, fontweight='bold')

# plt.hist(valores_a, bins=20, edgecolor='purple')
plt.xlabel('Municipios')
plt.ylabel('Precipitación en mm')
# plt.hist(valores_a, bins=10)
# plt.axvline(np.mean(valores_a), ymin=0.0, ymax=0.9,color='r')
plt.title('Histograma de los valores observados')
plt.grid(True)
plt.show()

# meses = df['valorobservado'].unique()
# print(valores)

## Mapa de las estaciones que registraron datos de precipitación

df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')

mapa = folium.Map(
    location=[
        df['latitud'].mean(), 
        df['longitud'].mean()
    ], 
    zoom_start=12
)

# Añadir un marcador por cada estación
for indice, fila in df.iterrows():
    folium.Marker(
        location=[fila['latitud'], fila['longitud']],
        popup=fila['nombreestacion']
    ).add_to(mapa)

mapa.save('mapa.html')