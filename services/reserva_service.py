#importaciones importantes
import json
import os
from models.reserva import Reserva
from utils.logger import Logger       
# ===================== RESERVA SERVICE =====================
class ReservaService:

    FILE_PATH = "data/storage/reservas.json"

    def __init__(self, cliente_repo, logger):
        self.cliente_repo = cliente_repo
        self.logger = logger
        self.reservas = []
        self.contador_reservas = 0

        os.makedirs("data/storage", exist_ok=True)

        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                json.dump([], f)

        self.cargar_contador()

    # ---------------- cargar contador ----------------
    def cargar_contador(self):
        try:
            with open(self.FILE_PATH, "r") as f:
                data = json.load(f)

            if data:
                ultimo_id = data[-1]["id"]
                numero = int(ultimo_id.split("-")[1])
                self.contador_reservas = numero
            else:
                self.contador_reservas = 0

        except Exception:
            self.contador_reservas = 0

    # ---------------- lista de reservas ----------------
    def lista_reservas(self):
        with open(self.FILE_PATH, "r") as f:
            return json.load(f)

    # ----------------validar duplicads ----------------
    def es_reserva_duplicada(self, id_cliente):

        reservas_json = self.lista_reservas()

        for r in reservas_json:
            if r["cliente_id"] == id_cliente:
                return True

        for r in self.reservas:
            if r.cliente == id_cliente:
                return True

        return False

    # ----------------crear reserva ----------------
    def crear_reservas(self, id_cliente, servicios, fecha, total):

        try:

            #validar servicios ----------------
            if not servicios or not isinstance(servicios, list):
                self.logger.log("ERROR", "Servicios inválidos")
                raise ValueError("Debe haber al menos un servicio")

            #validar cliente ----------------
            if not isinstance(id_cliente, int):
                self.logger.log("ERROR", f"Cliente inválido {id_cliente}")
                raise ValueError("Cliente no válido")

            #validar duplicado----------------
            if self.cliente_tiene_reserva_activa(id_cliente, fecha):

                self.logger.log(
                    "ERROR",
                    f"Cliente {id_cliente} intentó crear una reserva ya existente para la fecha {fecha}"
                )

                raise ValueError("Ya existe una reserva activa en esa fecha")

            #generar id ----------------
            self.contador_reservas += 1
            id_reserva = f"RES-{self.contador_reservas:04d}"

            # crear reserva ----------------
            reserva = Reserva(id_reserva, id_cliente, servicios, fecha, total)

            #guardar en memoria----------------
            self.reservas.append(reserva)

            #guardar en json----------------
            self.guardar_json(reserva)

            self.logger.log("INFO", f"Reserva creada ID {id_reserva}")

            return reserva

        except Exception as e:
            self.logger.log("ERROR", str(e))
            raise

    #guardar----------------
    def guardar_json(self, reserva):

        with open(self.FILE_PATH, "r") as f:
            data = json.load(f)

        data.append({
            "id": reserva.id,
            "cliente_id": reserva.cliente,
            "servicios": [s.__dict__ for s in reserva.servicio],  #lista de servicios
            "fecha": str(reserva.fecha),
            "estado": reserva.estado,
            "total": reserva.total
        })

        with open(self.FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    #cambio de estado ----------------
    def cambiar_estado_reserva(self, id_reserva, estado):

        try:
            with open(self.FILE_PATH, "r") as f:
                data = json.load(f)

            for reserva in data:
                if reserva["id"] == id_reserva:

                    if reserva["estado"] == estado:
                        self.logger.log(
                            "WARNING",
                            "Intento de asignar el mismo estado"
                        )
                        return

                    reserva["estado"] = estado
                    break
            else:
                self.logger.log("ERROR", "Reserva no encontrada")
                return

            with open(self.FILE_PATH, "w") as f:
                json.dump(data, f, indent=4)

            self.logger.log("INFO", f"Estado de la reserva: {id_reserva} ha sido cambiado a {estado}")

        except Exception as e:
            self.logger.log("ERROR", str(e))
        
    #------------------obtener reservas registradas-----------------------
    
    def obtener_reservas(self):

        try:
            with open(self.FILE_PATH, "r") as f:
                data = json.load(f)

            return data   

        except Exception as e:
            self.logger.log("ERROR", f"Error leyendo reservas: {e}")
            return []
        
    #----------------------------Validar reservas duplicadas-----------------------
    
    def cliente_tiene_reserva_activa(self, id_cliente, fecha):

        reservas = self.lista_reservas()

        for r in reservas:

            if (
                r["cliente_id"] == id_cliente and
                r["fecha"] == str(fecha) and
                r["estado"] in ["pendiente", "confirmada"]
            ):
                return True

        return False
            
