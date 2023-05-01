import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fdp(archivo, bins):
    data_frame = pd.read_excel(archivo)
    datos = data_frame['Datos'].tolist()
    return np.histogram(datos, bins=bins, density=True)

def valor_segun_fdp(bin_edges, counts):
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    return np.random.choice(bin_centers, p=counts/counts.sum())

counts_turnos, bin_edges_turnos = fdp('intervalos entre turnos.xlsx', 40)
counts_comandos, bin_edges_comandos = fdp('cantidad de comandos.xlsx', 10)
count_duracion, bin_edges_duracion = fdp('duracion de comandos.xlsx', 20)


def nuevo_intervalo_entre_turnos():
    return valor_segun_fdp(bin_edges_turnos, counts_turnos)

def nueva_cantidad_de_comandos():
    return valor_segun_fdp(bin_edges_comandos, counts_comandos)

def nueva_duracion_de_comando():
    return valor_segun_fdp(bin_edges_duracion, count_duracion)