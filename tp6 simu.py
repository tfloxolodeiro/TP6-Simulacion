import pandas as pd
from scipy import stats

def fdp(archivo):
    data_frame = pd.read_excel(archivo)
    datos = data_frame['Datos'].values
    return stats.gaussian_kde(datos)


def valor_segun_fdp(kde):
    return kde.resample(1)[0][0]

fdp_intervalo_turnos= fdp('intervalos entre turnos.xlsx')
fdp_cantidad_comandos = fdp('cantidad de comandos.xlsx')
fdp_duracion_comando = fdp('duracion de comandos.xlsx')


def nuevo_intervalo_entre_turnos():
    return valor_segun_fdp(fdp_intervalo_turnos)

def nueva_cantidad_de_comandos():
    return int(valor_segun_fdp(fdp_cantidad_comandos))

def nueva_duracion_de_comando():
    return valor_segun_fdp(fdp_duracion_comando)

print(nueva_cantidad_de_comandos())
print(nueva_cantidad_de_comandos())
print(nueva_cantidad_de_comandos())

valores = []

for i in range(999):
    valores.append(nuevo_intervalo_entre_turnos())

print ("Intervalo entre turnos:", sum(valores) / len(valores))

valores = []

for i in range(999):
    valores.append(nueva_cantidad_de_comandos())

print ("Cantidad de comandos:", sum(valores) / len(valores))

valores = []

for i in range(999):
    valores.append(nueva_duracion_de_comando())

print ("Duracion de comandos:", sum(valores) / len(valores))