from fdps import nuevo_intervalo_entre_turnos
from instancia import Instancia
import pantalla
from typing_extensions import TypedDict
import random

cantidad_instancias_premium: int = 1
cantidad_instancias_comunes: int = 2

Variables = TypedDict('Variables', {"tiempo_actual": float, "tiempo_final": float, "tiempo_proximo_turno": float, "espera_total": float, "turnos_totales": int, "suma_inicio_tiempo_espera_cola_premium": float, "suma_fin_tiempo_espera_cola_premium": float, "cola_premium": int, "cola_comun": int, "instancias_comunes": list[Instancia], "instancias_premium": list[Instancia], "suma_inicio_tiempo_espera_cola_comun": float, "suma_fin_tiempo_espera_cola_comun": float})

variables_simulacion: Variables = {
    "tiempo_actual": 0,
    "tiempo_final": 86400, #1 dia
    "cantidad_instancias_premium": cantidad_instancias_premium, #Control
    "cantidad_instancias_comunes": cantidad_instancias_comunes, #control
    "instancias_comunes": [Instancia(i, False) for i in range(cantidad_instancias_comunes)], #Estado
    "instancias_premium": [Instancia(i, True) for i in range(cantidad_instancias_premium)], #Estado
    "tiempo_proximo_turno": nuevo_intervalo_entre_turnos(), #Evento futuro
    "espera_total": 0,
    "turnos_totales": 0,
    "suma_inicio_tiempo_espera_cola_premium": 0,
    "suma_inicio_tiempo_espera_cola_comun": 0,
    "suma_fin_tiempo_espera_cola_premium": 0,
    "suma_fin_tiempo_espera_cola_comun": 0,
    "cola_premium": 0, #Estado
    "cola_comun": 0 #Estado


}

def instancia_con_proxima_salida() -> Instancia:
    instancias = variables_simulacion["instancias_comunes"] + variables_simulacion["instancias_premium"]
    return min(instancias, key=Instancia.get_proxima_salida)

def instancias_libres() -> list[Instancia]:
    return list(filter(Instancia.esta_libre, variables_simulacion["instancias_comunes"] + variables_simulacion["instancias_premium"] ))

def es_premium():
    return random.random() < 0.25

def instancias_premium_libres():
    return list(filter(Instancia.get_es_premium, instancias_libres()))

def instancias_comunes_libres():
    return list(filter(Instancia.es_comun, instancias_libres()))

def llegada_premium(tiempo_actual: float):
    global variables_simulacion
    premium_libres = instancias_premium_libres()
    comun_libres = instancias_comunes_libres()

    if len(premium_libres) > 0:
        premium_libres[0].atender(tiempo_actual)
    elif len(comun_libres) > 0:
        comun_libres[0].atender(tiempo_actual)
    else:
        variables_simulacion["cola_premium"] += 1
        variables_simulacion["suma_inicio_tiempo_espera_cola_premium"] += tiempo_actual

def llegada_comun(tiempo_actual: float):
    global variables_simulacion
    comun_libres = instancias_comunes_libres()

    if len(comun_libres) > 0:
        comun_libres[0].atender(tiempo_actual)
    else:
        variables_simulacion["cola_comun"] += 1
        variables_simulacion["suma_inicio_tiempo_espera_cola_comun"] += tiempo_actual

def llegada_turno(tiempo_llegada: float):
    global variables_simulacion
    variables_simulacion["tiempo_actual"] = tiempo_llegada
    variables_simulacion["tiempo_proximo_turno"] += nuevo_intervalo_entre_turnos()
    variables_simulacion["turnos_totales"] += 1

    if es_premium():
        llegada_premium(tiempo_llegada)
    else:
        llegada_comun(tiempo_llegada)


def tomar_de_cola_si_hay(nombre_cola: str, instancia: Instancia):
    global variables_simulacion
    tiempo_actual = variables_simulacion["tiempo_actual"]

    if(variables_simulacion[nombre_cola]  > 0):
        variables_simulacion[nombre_cola] -= 1
        variables_simulacion["suma_fin_tiempo_espera_" + nombre_cola] += tiempo_actual
        instancia.atender(tiempo_actual)


def salida(instancia: Instancia):
    global variables_simulacion
    variables_simulacion["tiempo_actual"] = instancia.get_proxima_salida()
    tiempo_actual = variables_simulacion["tiempo_actual"]
    instancia.terminarDeAtender(tiempo_actual)

    tomar_de_cola_si_hay("cola_premium", instancia) #Las premium y comunes siempre checkean la premium primero

    if(instancia.es_comun() and instancia.esta_libre()): #Si es comun y no tomo a nadie premium
        tomar_de_cola_si_hay("cola_comun", instancia) 

def hay_personas_esperando():
    return variables_simulacion["cola_premium"] > 0 or variables_simulacion["cola_comun"] > 0

def ciclo_de_evento():
    global variables_simulacion
    tiempo_actual = variables_simulacion["tiempo_actual"]
    tiempo_final = variables_simulacion["tiempo_final"]
    proximo_turno = variables_simulacion["tiempo_proximo_turno"]
    proxima_instancia = instancia_con_proxima_salida()

    if(tiempo_actual < tiempo_final or hay_personas_esperando()):
        if(proximo_turno < proxima_instancia.get_proxima_salida()):
            llegada_turno(proximo_turno)
        else:
            salida(proxima_instancia)
    
    if(tiempo_actual > tiempo_final): #Vaciamiento
        variables_simulacion["tiempo_proximo_turno"] = float("inf")


def main():
    while(True):
        ciclo_de_evento()
        pantalla.actualizar_pantalla(variables_simulacion)

if __name__ == "__main__":
    main()