#importaciones importantes
from models.cliente import Cliente
from utils.logger import Logger
import json
import os

#-------------------------------------------------------------------
  #-----------------------Manejo de datos de clientes-------------------
  #-------------------------------------------------------------------   
class ClienteDuplicadoError(Exception):
    pass


class RepositorioError(Exception):
    pass
    
class ClienteRepository:

    FILE_PATH = "data/storage/clientes.json"

    def __init__(self):
        os.makedirs("data/storage", exist_ok=True)
        self.logger = Logger()

        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                json.dump([], f)

    def get_clientes_registrados(self):
        try:
            with open(self.FILE_PATH, "r") as f:
                data = json.load(f)

            return [
                Cliente(
                    c["id"],
                    c["nombre"],
                    c["telefono"],
                    c["email"],
                    c["tipo"]
                )
                for c in data
            ]

        except Exception as e:
            self.logger.log("ERROR", f"Error leyendo clientes: {e}")
            raise RepositorioError("No se pudieron leer clientes")

    def save_cliente(self, cliente):

        try:
            with open(self.FILE_PATH, "r") as f:
                data = json.load(f)

            # duplicados
            if any(c["id"] == cliente.id for c in data):
                self.logger.log("ERROR", f"Cliente duplicado ID {cliente.id}")
                raise ClienteDuplicadoError("Cliente ya existe")

            data.append({
                "id": cliente.id,
                "nombre": cliente.nombre,
                "telefono": cliente.telefono,
                "email": cliente.email,
                "tipo": cliente.tipo
            })

            with open(self.FILE_PATH, "w") as f:
                json.dump(data, f, indent=4)

        except ClienteDuplicadoError:
            raise

        except Exception as e:
            self.logger.log("ERROR", f"Error guardando cliente: {e}")
            raise RepositorioError("Error en almacenamiento")

        else:
            self.logger.log("INFO", f"Cliente guardado ID {cliente.id}")