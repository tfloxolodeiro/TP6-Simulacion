from fdps import nuevo_intervalo_entre_turnos, nueva_cantidad_de_comandos, nueva_duracion_de_comando
import numpy
import pantalla

tiempo_actual: float = 0
tiempo_final: float = 999999999 #Ponele

#control
cantidad_de_instancias: int = 10

#estado
TC_de_instancias = numpy.array([0] * cantidad_de_instancias) #El array de numpy es para poder usar algunos metodos mas power.

#eventos futuros
tiempo_proximo_turno: float = nuevo_intervalo_entre_turnos() #Inicializa con un turno


def nuevo_tiempo_uso_del_bot() -> float:
    cantidad_comandos: int = nueva_cantidad_de_comandos()
    tiempo_de_uso: float = 0
    for i in range(cantidad_comandos):
        tiempo_de_uso += nueva_duracion_de_comando() #Esto es valido? En la realidad la duracion del comando se deberia saber al ejecutarlo, no al pedir el turno.

    return tiempo_de_uso 


def indice_menor_TC() -> float:
    return TC_de_instancias.argmin()


def asignar_uso_a_instancia(tiempo_de_uso: float, indice_instancia: int):
    global TC_de_instancias

    TC_instancia = TC_de_instancias[indice_instancia]

    if(tiempo_actual >= TC_instancia):
        TC_de_instancias[indice_instancia] = tiempo_actual + tiempo_de_uso
    else:
        TC_de_instancias[indice_instancia] += tiempo_de_uso


def ciclo_de_evento():
    global tiempo_actual #Segun lo que entiendo, esto sirve para decirle a python que vamos a modificar la variable global y no crear una nueva en esta funcion.
    global tiempo_proximo_turno 

    tiempo_actual = tiempo_proximo_turno
    tiempo_proximo_turno += nuevo_intervalo_entre_turnos()

    tiempo_de_uso = nuevo_tiempo_uso_del_bot()
    instancia_con_menor_TC = indice_menor_TC()

    asignar_uso_a_instancia(tiempo_de_uso, instancia_con_menor_TC)

def main():
    while(tiempo_actual < tiempo_final):
        ciclo_de_evento()
        pantalla.actualizar_pantalla(tiempo_actual, TC_de_instancias)

if __name__ == "__main__":
    main()