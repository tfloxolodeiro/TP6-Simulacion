import pandas as pd
from scipy import stats

def fdp(archivo: str):
    data_frame = pd.read_excel(archivo)
    datos = data_frame['Datos'].values
    return stats.gaussian_kde(datos)

def valor_segun_fdp(fdp):
    return fdp.resample(1)[0][0]

fdp_intervalo_turnos = fdp('intervalos entre turnos.xlsx')
fdp_cantidad_comandos = fdp('cantidad de comandos.xlsx')
fdp_duracion_comando = fdp('duracion de comandos.xlsx')

def nuevo_intervalo_entre_turnos() -> float:
    return valor_segun_fdp(fdp_intervalo_turnos)

def nueva_cantidad_de_comandos() -> int:
    return int(valor_segun_fdp(fdp_cantidad_comandos))

def nueva_duracion_de_comando() -> float:
    return valor_segun_fdp(fdp_duracion_comando)

