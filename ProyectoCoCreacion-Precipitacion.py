
from sodapy import Socrata
import datetime 

datasetId = "s54a-sgyg"

cliente=Socrata('www.datos.gov.co', None)
totalRegistros = cliente.get(datasetId, select="COUNT(*)")[0]["COUNT"]
if(int(totalRegistros) > 1000000):
    print("Inicio recuperación de datos" + str(datetime.datetime.now()))
    result=cliente.get(datasetId, limit=1000000)
    print("Fin recuperación de datos" + str(datetime.datetime.now()))
else:
    print("Inicio recuperación de datos" + str(datetime.datetime.now()))
    result=cliente.get(datasetId, limit=totalRegistros)
    print("Fin recuperación de datos" + str(datetime.datetime.now()))

