
from sodapy import Socrata
import datetime
from dateutil.relativedelta import relativedelta    
import pandas as pd

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
limiteInferior = (datetime.datetime.now() - relativedelta(months=3)).date()

#Se define el valor del departamento a filtrar.
Departamento = "BOYACÁ"

#Se construye el filtro para la petición al API
consulta = f"departamento = '{Departamento}' AND fechaobservacion >= '{limiteInferior}'"

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

#Se realiza una verificación de los datos antes de aplicar una limpieza de registros con datos nulos
df.info()
df = df.dropna(axis=0,how='any')
df.info()

# df.info()