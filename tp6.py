from fdps import nuevo_intervalo_entre_turnos
from instancia import Instancia
import pantalla
from typing_extensions import TypedDict

cantidad_de_instancias: int = 4

Variables = TypedDict('Variables', {"tiempo_actual": float, "tiempo_final": float, "cantidad_de_instancias": int, "instancias_bot": list[Instancia], "tiempo_proximo_turno": float, "espera_total": float, "turnos_totales": int, "suma_inicio_tiempo_espera": float, "suma_fin_tiempo_espera": float, "cola": int} )

variables_simulacion: Variables = {
    "tiempo_actual": 0,
    "tiempo_final": 86400, #1 dia
    "cantidad_de_instancias": cantidad_de_instancias, #Control
    "instancias_bot": [Instancia(i) for i in range(cantidad_de_instancias)], #Estado
    "tiempo_proximo_turno": nuevo_intervalo_entre_turnos(), #Evento futuro
    "espera_total": 0,
    "turnos_totales": 0,
    "suma_inicio_tiempo_espera": 0,
    "suma_fin_tiempo_espera": 0,
    "cola": 0,


}

def instancia_con_proxima_salida() -> Instancia:
    return min(variables_simulacion["instancias_bot"], key=Instancia.get_proxima_salida)

def instancias_libres() -> list[Instancia]:
    return list(filter(Instancia.esta_libre, variables_simulacion["instancias_bot"]))

def llegada_turno(tiempo_llegada: float):
    global variables_simulacion
    variables_simulacion["tiempo_actual"] = tiempo_llegada
    variables_simulacion["tiempo_proximo_turno"] += nuevo_intervalo_entre_turnos()
    variables_simulacion["turnos_totales"] += 1

    inst_libres = instancias_libres()

    if (len(inst_libres) > 0):
        inst_libres[0].atender(tiempo_llegada)
    else:
        variables_simulacion["cola"] += 1
        variables_simulacion["suma_inicio_tiempo_espera"] += tiempo_llegada


def salida(instancia: Instancia):
    global variables_simulacion
    variables_simulacion["tiempo_actual"] = instancia.get_proxima_salida()
    tiempo_actual = variables_simulacion["tiempo_actual"]
    instancia.terminarDeAtender(tiempo_actual)

    if(variables_simulacion["cola"]  > 0):
        variables_simulacion["cola"] -= 1
        variables_simulacion["suma_fin_tiempo_espera"] += tiempo_actual
        instancia.atender(tiempo_actual)


def ciclo_de_evento():
    global variables_simulacion
    tiempo_actual = variables_simulacion["tiempo_actual"]
    tiempo_final = variables_simulacion["tiempo_final"]
    proximo_turno = variables_simulacion["tiempo_proximo_turno"]
    proxima_instancia = instancia_con_proxima_salida()

    if(tiempo_actual < tiempo_final or variables_simulacion["cola"] > 0):
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