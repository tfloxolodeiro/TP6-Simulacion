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
    + [[sg.Text('Tiempo ocioso total: '), sg.Text(key='OCIOSO_TOTAL')]] \
    + [[sg.Button('CERRAR')]]

window = sg.Window('TP Simulacion :)', layout)

def actualizar_pantalla(tiempo_actual: float, instancias: list[Instancia]):
    event = window.read(1)  

    if 'CERRAR' in event :
        window.Close()
        exit()

    actualizar_tiempo_actual(tiempo_actual)
    actualizar_instancias(instancias, tiempo_actual)
    actualizar_tiempo_ocioso_total(instancias, tiempo_actual)
    window.refresh()

def actualizar_tiempo_ocioso_total(instancias: list[Instancia], tiempo_actual: float):
    tiempo_ocioso_total: int = int(sum(map(Instancia.get_tiempo_ocioso, instancias)))
    tiempo_total: float = tiempo_actual * len(instancias) #Es el tiempo entre todas las instancias
    tiempo_ocioso_porcentual: float = round( tiempo_ocioso_total / tiempo_total  * 100, 2) 
    texto_ocioso: str = str(tiempo_ocioso_total) + ' (' + str(tiempo_ocioso_porcentual) + '%)'

    window['OCIOSO_TOTAL'].update(texto_ocioso)

def actualizar_tiempo_actual(tiempo_actual: float):
    window['-TIEMPO-'].update(int(tiempo_actual))
    window['-PORCENTAJE_COMPLETO-'].update(texto_porcentaje_completitud(tiempo_actual))

def actualizar_instancias(instancias: list[Instancia], tiempo_actual: float):
    for instancia in instancias:
        window['INSTANCIA_' + str(instancia.get_id())].update(int(instancia.get_tiempo_comprometido()))
        window['OCIOSO_' + str(instancia.get_id())].update(instancia.texto_tiempo_ocioso(tiempo_actual))

def texto_porcentaje_completitud(tiempo_actual) -> str:
    porcentaje_completitud: float = round(tiempo_actual/tp6.tiempo_final * 100, 2)
    return '(' + str(porcentaje_completitud) + '%)' 