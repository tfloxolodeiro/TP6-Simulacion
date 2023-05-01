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
    [sg.Text('Tiempo actual: '), sg.Text(key='-TIEMPO-'), sg.Text(key='-PORCENTAJE_COMPLETO-')]] \
    + layout_instancias  \
    + [[sg.Text('RESULTADOS')]] \
    + layout_ocioso_instancias \
    + [[sg.Button('CERRAR')]]
    

window = sg.Window('TP Simulacion :)', layout)

def actualizar_pantalla(tiempo_actual: float, instancias: list[Instancia]):
    event = window.read(1)  

    if 'CERRAR' in event :
        window.Close()
        exit()

    window['-TIEMPO-'].update(int(tiempo_actual))
    window['-PORCENTAJE_COMPLETO-'].update(texto_porcentaje_completitud(tiempo_actual))
    actualizar_instancias(instancias, tiempo_actual)
    window.refresh()

def actualizar_instancias(instancias: list[Instancia], tiempo_actual: float):
    for instancia in instancias:
        window['INSTANCIA_' + str(instancia.get_id())].update(int(instancia.get_tiempo_comprometido()))
        window['OCIOSO_' + str(instancia.get_id())].update(instancia.texto_tiempo_ocioso(tiempo_actual))

def texto_porcentaje_completitud(tiempo_actual) -> str:
    porcentaje_completitud: float = round(tiempo_actual/tp6.tiempo_final * 100, 2)
    return '(' + str(porcentaje_completitud) + '%)' 