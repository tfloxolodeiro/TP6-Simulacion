import PySimpleGUI as sg
from instancia import Instancia
import tp6

def indice_a_layout_instancia(indice: int, tag: str):
    return [sg.Text(tag + ' TPS Instancia ' + str(indice) + ': '), sg.Text(key=('INSTANCIA_' + tag + '_' + str(indice)))]

def layout_premium(indice: int):
    return indice_a_layout_instancia(indice, "[P]")

def layout_comun(indice: int):
    return indice_a_layout_instancia(indice, "[C]")

def indice_a_layout_ocioso_de_instancia(indice: int, tag: str):
    return [sg.Text(tag + ' Tiempo ocioso instancia ' + str(indice) + ':'), sg.Text(key=('OCIOSO_' + tag + '_' + str(indice)))]

def ocioso_de_instancia_premium(indice: int):
    return indice_a_layout_ocioso_de_instancia(indice, "[P]")

def ocioso_de_instancia_comun(indice: int):
    return indice_a_layout_ocioso_de_instancia(indice, "[C]")


layout_instancias_premium = list(map(layout_premium, range(tp6.cantidad_instancias_premium)))
layout_instancias_comunes = list(map(layout_comun, range(tp6.cantidad_instancias_comunes)))


layout_ocioso_instancias_premium = list(map(ocioso_de_instancia_premium, range(tp6.cantidad_instancias_premium)))
layout_ocioso_instancias_comunes = list(map(ocioso_de_instancia_comun, range(tp6.cantidad_instancias_comunes)))

layout = [
    [[sg.Text('ESTADO', background_color='Black')]] \
    + [sg.Text('Tiempo actual: '), sg.Text(key='-TIEMPO-'), sg.Text(key='-PORCENTAJE_COMPLETO-')]] \
    + [[sg.Text('Cola premium: '), sg.Text(key='COLA_PREMIUM')]] \
    + [[sg.Text('Cola comun: '), sg.Text(key='COLA_COMUN')]] \
    + layout_instancias_premium + layout_instancias_comunes \
    + [[sg.Text('RESULTADOS', background_color='Black')]] \
    + layout_ocioso_instancias_premium + layout_ocioso_instancias_comunes\
    + [[sg.Text('Porcentaje tiempo ocioso: '), sg.Text(key='OCIOSO_TOTAL')]] \
    + [[sg.Text('Promedio tiempo de espera premium: '), sg.Text(key='PROMEDIO_ESPERA_PREMIUM')]] \
    + [[sg.Text('Promedio tiempo de espera comun: '), sg.Text(key='PROMEDIO_ESPERA_COMUN')]] \
    + [[sg.Button('CERRAR')]]

window = sg.Window('TP Simulacion :)', layout)

def actualizar_pantalla(variables: tp6.Variables):
    event = window.read(1)  

    if 'CERRAR' in event :
        window.Close()
        exit()

    actualizar_tiempo_actual(variables)
    actualizar_cola(variables)
    actualizar_instancias(variables)
    actualizar_tiempo_ocioso(variables)
    actualizar_tiempo_espera(variables)
    window.refresh()

def actualizar_tiempo_espera(variables: tp6.Variables):
    espera_total_premium = variables["suma_fin_tiempo_espera_cola_premium"] - variables["suma_inicio_tiempo_espera_cola_premium"]
    espera_total_comun = variables["suma_fin_tiempo_espera_cola_comun"] - variables["suma_inicio_tiempo_espera_cola_comun"]
    turnos_totales = variables['turnos_totales']
    promedio_espera_premium = espera_total_premium / turnos_totales
    promedio_espera_comun = espera_total_comun / turnos_totales

    window['PROMEDIO_ESPERA_PREMIUM'].update(str(int(promedio_espera_premium)))
    window['PROMEDIO_ESPERA_COMUN'].update(str(int(promedio_espera_comun)))

def actualizar_tiempo_ocioso(variables: tp6.Variables):
    tiempo_ocioso_porcentual: float = porcentaje_tiempo_ocioso(variables)
    texto_ocioso: str = pretty_porcentaje(tiempo_ocioso_porcentual)

    window['OCIOSO_TOTAL'].update(texto_ocioso)

def porcentaje_tiempo_ocioso(variables: tp6.Variables):
    instancias = variables['instancias_comunes'] + variables['instancias_premium'] 
    tiempo_actual = variables['tiempo_actual']

    tiempo_ocioso_total: int = int(sum(map(Instancia.get_tiempo_ocioso, instancias)))
    tiempo_total: float = tiempo_actual * len(instancias) #Es el tiempo entre todas las instancias
    return round( tiempo_ocioso_total / tiempo_total  * 100, 2) 

def actualizar_cola(variables: tp6.Variables):
    window['COLA_PREMIUM'].update(variables['cola_premium'])
    window['COLA_COMUN'].update(variables['cola_comun'])

def actualizar_tiempo_actual(variables: tp6.Variables):
    tiempo_actual = variables['tiempo_actual']

    window['-TIEMPO-'].update(int(tiempo_actual))
    window['-PORCENTAJE_COMPLETO-'].update(texto_porcentaje_completitud(variables))

def actualizar_instancias(variables: tp6.Variables):
    instancias_comunes = variables["instancias_comunes"]
    instancias_premium = variables["instancias_premium"]
    tiempo_actual = variables["tiempo_actual"]

    for instancia in instancias_comunes:
        window['INSTANCIA_[C]_' + str(instancia.get_id())].update(instancia.texto_tiempo_salida())
        window['OCIOSO_[C]_' + str(instancia.get_id())].update(instancia.texto_tiempo_ocioso(tiempo_actual))

    for instancia in instancias_premium:
        window['INSTANCIA_[P]_' + str(instancia.get_id())].update(instancia.texto_tiempo_salida())
        window['OCIOSO_[P]_' + str(instancia.get_id())].update(instancia.texto_tiempo_ocioso(tiempo_actual))

def texto_porcentaje_completitud(variables: tp6.Variables) -> str:
    tiempo_actual = variables["tiempo_actual"]
    tiempo_final = variables["tiempo_final"]
    
    porcentaje_completitud: float = round(tiempo_actual/tiempo_final * 100, 2)
    return pretty_porcentaje(porcentaje_completitud)

def pretty_porcentaje(porcentaje: float) -> str:
    return '(' + str(porcentaje) + '%)' 