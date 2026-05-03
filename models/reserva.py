#importaciones importantes
from datetime import datetime
        
 #-------------------------------------------------------------------
  #-----------------------Reservas-------------------
  #-------------------------------------------------------------------   
  
class Reserva:
    def __init__(self, id, cliente, servicio, fecha, total):
        self.id = id
        self.cliente = cliente
        self.servicio = servicio
        self.fecha = fecha
        self.estado = "pendiente"
        self.total = total

    # ---------------- ID ----------------
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value


    # ---------------- CLIENTE ----------------
    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, valor):
        if valor is None:
            raise ValueError("Cliente no puede ser vacío")
        self.__cliente = valor

    # ---------------- SERVICIO ----------------
    @property
    def servicio(self):
        return self.__servicio

    @servicio.setter
    def servicio(self, valor):
        if valor is None:
            raise ValueError("Servicio no puede ser vacío")
        self.__servicio = valor

    # ---------------- FECHA ----------------
    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, valor):
        if not isinstance(valor, str):
            raise ValueError("La fecha debe ser texto YYYY-MM-DD")

        try:
            self.__fecha = datetime.strptime(valor, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato inválido. Use YYYY-MM-DD")

    # ---------------- ESTADO ----------------
    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        estados_validos = ["pendiente", "confirmado", "cancelado"]

        if not isinstance(valor, str):
            raise ValueError("Estado debe ser texto")

        valor = valor.lower().strip()

        if valor not in estados_validos:
            raise ValueError(f"Estado inválido: {estados_validos}")

        self.__estado = valor

    # ---------------- COMPORTAMIENTO ----------------

    def confirmar(self):
        self.estado = "confirmado"

    def cancelar(self):
        self.estado = "cancelado"

    def describir(self):
        servicios_txt = ", ".join(self.servicio) if isinstance(self.servicio, list) else self.servicio

        return (
            f"Reserva ID: {self.id} | "
            f"Cliente ID: {self.cliente} | "
            f"Servicios: {servicios_txt} | "
            f"Fecha: {self.fecha} | "
            f"Estado: {self.estado} | "
            f"Total: {self.total}"
        )