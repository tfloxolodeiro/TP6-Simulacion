from fdps import nuevo_intervalo_entre_turnos, nueva_cantidad_de_comandos, nueva_duracion_de_comando
from instancia import Instancia
import pantalla
from typing_extensions import TypedDict

cantidad_de_instancias: int = 3

Variables = TypedDict('Variables', {"tiempo_actual": float, "tiempo_final": float, "cantidad_de_instancias": int, "instancias_bot": list[Instancia], "tiempo_proximo_turno": float, "espera_total": float, "turnos_totales": int} )

variables_simulacion: Variables = {
    "tiempo_actual": 0,
    "tiempo_final": 86400, #1 dia
    "cantidad_de_instancias": cantidad_de_instancias, #Control
    "instancias_bot": [Instancia(i) for i in range(cantidad_de_instancias)], #Estado
    "tiempo_proximo_turno": nuevo_intervalo_entre_turnos(), #Evento futuro
    "espera_total": 0,
    "turnos_totales": 0

}

def nuevo_tiempo_uso_del_bot() -> float:
    cantidad_comandos: int = nueva_cantidad_de_comandos()
    tiempo_de_uso: float = 0
    for i in range(cantidad_comandos):
        tiempo_de_uso += nueva_duracion_de_comando() #Esto es valido? En la realidad la duracion del comando se deberia saber al ejecutarlo, no al pedir el turno.

    return tiempo_de_uso 


def instancia_con_menor_TC() -> float:
    return min(variables_simulacion["instancias_bot"], key=Instancia.get_tiempo_comprometido)


def ciclo_de_evento():
    global variables_simulacion
    tiempo_actual = variables_simulacion["tiempo_actual"]
    tiempo_final = variables_simulacion["tiempo_final"]
    proximo_turno = variables_simulacion["tiempo_proximo_turno"]

    if(tiempo_actual < tiempo_final):
        variables_simulacion["tiempo_actual"] = proximo_turno
        variables_simulacion["turnos_totales"] += 1
        variables_simulacion["tiempo_proximo_turno"] += nuevo_intervalo_entre_turnos()


        instancia_asignada = instancia_con_menor_TC()
        variables_simulacion["espera_total"] += instancia_asignada.espera_hasta_disponibilidad(tiempo_actual)
        
        tiempo_de_uso = nuevo_tiempo_uso_del_bot()
        instancia_asignada.asignar_tiempo(tiempo_de_uso, tiempo_actual)

def main():
    while(True):
        ciclo_de_evento()
        pantalla.actualizar_pantalla(variables_simulacion)

if __name__ == "__main__":
    main()