from fdps import nueva_cantidad_de_comandos, nueva_duracion_de_comando


def nuevo_tiempo_uso_del_bot() -> float:
    cantidad_comandos: int = nueva_cantidad_de_comandos()
    tiempo_de_uso: float = 0
    for i in range(cantidad_comandos):
        tiempo_de_uso += nueva_duracion_de_comando() #Esto es valido? En la realidad la duracion del comando se deberia saber al ejecutarlo, no al pedir el turno.

    return tiempo_de_uso 

class Instancia:
    id: int
    proxima_salida: float = float("inf") #High value
    tiempo_ocioso: float = 0
    inicio_tiempo_ocioso: float = 0

    def __init__(self, id):
        self.id = id

    def atender(self, tiempo_actual: float):
        self.tiempo_ocioso += tiempo_actual - self.inicio_tiempo_ocioso
        self.proxima_salida = tiempo_actual + nuevo_tiempo_uso_del_bot()        

    def terminarDeAtender(self, tiempo_actual: float):
        self.inicio_tiempo_ocioso = tiempo_actual
        self.proxima_salida = float("inf")

    def texto_tiempo_ocioso(self, tiempo_actual: float):
        porcentaje_ocioso: float = round(self.tiempo_ocioso / tiempo_actual * 100, 2)
        return str(int(self.tiempo_ocioso)) + ' (' + str(porcentaje_ocioso) + '%)'

    def texto_tiempo_salida(self):
        if(self.esta_libre()):
            return "Libre"
        else:
            return str(int(self.proxima_salida))

    def esta_libre(self):
        return self.proxima_salida == float("inf")

    def get_proxima_salida(self):
        return self.proxima_salida
    
    def get_tiempo_ocioso(self):
        return self.tiempo_ocioso
    
    def get_id(self):
        return self.id
    
