class Instancia:
    id: int
    tiempo_comprometido: float = 0
    tiempo_ocioso: float = 0

    def __init__(self, id):
        self.id = id

    def asignar_tiempo(self, tiempo_de_uso: float, tiempo_actual: float):
        if(self.esta_ociosa(tiempo_actual)): 
            self.tiempo_ocioso += tiempo_actual - self.tiempo_comprometido
            self.tiempo_comprometido = tiempo_actual + tiempo_de_uso
        else: 
            self.tiempo_comprometido += tiempo_de_uso

    def esta_ociosa(self, tiempo_actual: float):
        return tiempo_actual >= self.tiempo_comprometido

    def espera_hasta_disponibilidad(self, tiempo_actual: float):
        return max(0, self.tiempo_comprometido - tiempo_actual)


    def texto_tiempo_ocioso(self, tiempo_actual: float):
        porcentaje_ocioso: float = round(self.tiempo_ocioso / tiempo_actual * 100, 2)
        return str(int(self.tiempo_ocioso)) + ' (' + str(porcentaje_ocioso) + '%)'

    def get_tiempo_comprometido(self):
        return self.tiempo_comprometido
    
    def get_tiempo_ocioso(self):
        return self.tiempo_ocioso
    
    def get_id(self):
        return self.id
    
