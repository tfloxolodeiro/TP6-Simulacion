import PySimpleGUI as sg
from instancia import Instancia
import tp6

def indice_a_layout_instancia(indice: int):
    return [sg.Text('TC instancia ' + str(indice) + ': '), sg.Text(key=('INSTANCIA_' + str(indice)))]

def indice_a_layout_ocioso_de_instancia(indice: int):
    return [sg.Text('Tiempo ocioso instancia ' + str(indice) + ':'), sg.Text(key=('OCIOSO_' + str(indice)))]

layout_instancias = list(map(indice_a_layout_instancia, range(tp6.cantidad_de_instancias)))
layout_ocioso_instancias = list(map(indice_a_layout_ocioso_de_instancia, range(tp6.cantidad_de_instancias)))

layout = [
    [[sg.Text('ESTADO', background_color='Black')]] \
    + [sg.Text('Tiempo actual: '), sg.Text(key='-TIEMPO-'), sg.Text(key='-PORCENTAJE_COMPLETO-')]] \
    + layout_instancias  \
    + [[sg.Text('RESULTADOS', background_color='Black')]] \
    + layout_ocioso_instancias \
    + [[sg.Text('Porcentaje tiempo ocioso: '), sg.Text(key='OCIOSO_TOTAL')]] \
    + [[sg.Button('CERRAR')]]

window = sg.Window('TP Simulacion :)', layout)

def actualizar_pantalla(variables: tp6.Variables):
    event = window.read(1)  

    if 'CERRAR' in event :
        window.Close()
        exit()

    actualizar_tiempo_actual(variables)
    actualizar_instancias(variables)
    actualizar_tiempo_ocioso(variables)
    window.refresh()

def actualizar_tiempo_ocioso(variables: tp6.Variables):
    tiempo_ocioso_porcentual: float = porcentaje_tiempo_ocioso(variables)
    texto_ocioso: str = '(' + str(tiempo_ocioso_porcentual) + '%)'

    window['OCIOSO_TOTAL'].update(texto_ocioso)

def porcentaje_tiempo_ocioso(variables: tp6.Variables):
    instancias = variables['instancias_bot']
    tiempo_actual = variables['tiempo_actual']

    tiempo_ocioso_total: int = int(sum(map(Instancia.get_tiempo_ocioso, instancias)))
    tiempo_total: float = tiempo_actual * len(instancias) #Es el tiempo entre todas las instancias
    return round( tiempo_ocioso_total / tiempo_total  * 100, 2) 

def actualizar_tiempo_actual(variables: tp6.Variables):
    tiempo_actual = variables['tiempo_actual']

    window['-TIEMPO-'].update(int(tiempo_actual))
    window['-PORCENTAJE_COMPLETO-'].update(texto_porcentaje_completitud(variables))

def actualizar_instancias(variables: tp6.Variables):
    instancias = variables["instancias_bot"]
    tiempo_actual = variables["tiempo_actual"]

    for instancia in instancias:
        window['INSTANCIA_' + str(instancia.get_id())].update(int(instancia.get_tiempo_comprometido()))
        window['OCIOSO_' + str(instancia.get_id())].update(instancia.texto_tiempo_ocioso(tiempo_actual))

def texto_porcentaje_completitud(variables: tp6.Variables) -> str:
    tiempo_actual = variables["tiempo_actual"]
    tiempo_final = variables["tiempo_final"]
    
    porcentaje_completitud: float = round(tiempo_actual/tiempo_final * 100, 2)
    return '(' + str(porcentaje_completitud) + '%)' 