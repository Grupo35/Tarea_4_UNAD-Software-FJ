# Importaciones necesarias para manejo de archivos y fecha/hora
import os
from datetime import datetime

#-------------------------------------------------------------------
#----------------------- SISTEMA DE LOGS ----------------------------
#-------------------------------------------------------------------   
class Logger:
    
    # Ruta donde se almacenará el archivo de registro (logs)
    FILE_PATH = "data/logs/logs.txt"
    
    def _init_(self):
        # Crea la carpeta de logs si no existe
        # Evita errores si la carpeta ya está creada
        os.makedirs("data/logs", exist_ok=True)
        
    def log(self, nivel, mensaje):
        # Obtiene la fecha y hora actual en formato año-mes-día hora:minuto:segundo
        tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Abre el archivo en modo agregar (no borra información previa)
        # Permite escribir caracteres especiales gracias a UTF-8
        with open(self.FILE_PATH, "a", encoding="utf-8") as f:
            # Guarda el mensaje con el formato: [fecha] NIVEL: mensaje
            f.write(f"[{tiempo}] {nivel}: {mensaje}\n")
    
    