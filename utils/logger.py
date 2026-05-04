#importaciones importantes
import os
from datetime import datetime

#-------------------------------------------------------------------
  #-----------------------LOG-------------------
  #-------------------------------------------------------------------   
class Logger:
    
    FILE_PATH = "data/logs/logs.txt"
    
    def _init_(self):
        os.makedirs("data/logs", exist_ok=True)
        
    def log(self, nivel, mensaje):
        tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{tiempo}] {nivel}: {mensaje}\n")