from matplotlib import pyplot as plt #No borrar, es usado en funcion comentada
import numpy as np #idem
import pandas as pd
from scipy import stats

data_frame = pd.read_excel("datos.xlsx")

def fdp(columna: str):
    datos = data_frame[columna].values
    return stats.gaussian_kde(datos)

def valor_segun_fdp(fdp):
    return fdp.resample(1)[0][0]

fdp_intervalo_turnos = fdp('IET') #Intervalo entre turnos
fdp_cantidad_comandos = fdp('CDC') #Cantidad de comandos
fdp_duracion_comando = fdp('DDC') #Duracion de comando

def nuevo_intervalo_entre_turnos() -> float:
    return valor_segun_fdp(fdp_intervalo_turnos)

def nueva_cantidad_de_comandos() -> int:
    return int(valor_segun_fdp(fdp_cantidad_comandos))

def nueva_duracion_de_comando() -> float:
    return valor_segun_fdp(fdp_duracion_comando)

"""
def graficar_fdp(fdp, minimo, maximo):
    x = np.linspace(minimo, maximo, 100)
    plt.plot(x, fdp(x))
    plt.show()

graficar_fdp(fdp_cantidad_comandos, 1, 10)
graficar_fdp(fdp_duracion_comando, 42, 136)
graficar_fdp(fdp_intervalo_turnos, 0, 599)
"""