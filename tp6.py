from fdps import nuevo_intervalo_entre_turnos, nueva_cantidad_de_comandos, nueva_duracion_de_comando
import numpy
from instancia import Instancia
import pantalla

tiempo_actual: float = 0
tiempo_final: float = 999999 #Ponele

#control
cantidad_de_instancias: int = 1

#estado
instancias: list[Instancia] = [Instancia(i) for i in range(cantidad_de_instancias)] #Tienen que ser instancias distintas de la clase asi que por eso el for en vez de usar el (*).

#evento futuro
tiempo_proximo_turno: float = nuevo_intervalo_entre_turnos() #Inicializa con un turno


def nuevo_tiempo_uso_del_bot() -> float:
    cantidad_comandos: int = nueva_cantidad_de_comandos()
    tiempo_de_uso: float = 0
    for i in range(cantidad_comandos):
        tiempo_de_uso += nueva_duracion_de_comando() #Esto es valido? En la realidad la duracion del comando se deberia saber al ejecutarlo, no al pedir el turno.

    return tiempo_de_uso 


def instancia_con_menor_TC() -> float:
    return min(instancias, key=Instancia.get_tiempo_comprometido)


def ciclo_de_evento():
    global tiempo_actual
    global tiempo_proximo_turno 

    if(tiempo_actual < tiempo_final):
        tiempo_actual = tiempo_proximo_turno
        tiempo_proximo_turno += nuevo_intervalo_entre_turnos()

        tiempo_de_uso = nuevo_tiempo_uso_del_bot()

        instancia_con_menor_TC().asignar_tiempo(tiempo_de_uso, tiempo_actual)

def main():
    while(True):
        ciclo_de_evento()
        pantalla.actualizar_pantalla(tiempo_actual, instancias)

if __name__ == "__main__":
    main()