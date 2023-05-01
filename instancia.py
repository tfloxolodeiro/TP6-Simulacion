class Instancia:
    id: int
    tiempo_comprometido: float = 0
    tiempo_ocioso: float = 0

    def __init__(self, id):
        self.id = id

    def asignar_tiempo(self, tiempo_de_uso: float, tiempo_actual: float):
        if(tiempo_actual >= self.tiempo_comprometido): #Estaba ocioso
            self.tiempo_ocioso += tiempo_actual - self.tiempo_comprometido
            self.tiempo_comprometido = tiempo_actual + tiempo_de_uso
        else: 
            self.tiempo_comprometido += tiempo_de_uso

    def get_tiempo_comprometido(self):
        return self.tiempo_comprometido
    
    def get_tiempo_ocioso(self):
        return self.tiempo_ocioso
    
    def get_id(self):
        return self.id
    
