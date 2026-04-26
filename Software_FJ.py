# ---------------- IMPORTACIONES ----------------
import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
import json
import os
import re
from datetime import datetime
from abc import ABC, abstractmethod

  #-------------------------------------------------------------------
  #-----------------------Servicios--------------------
  #-------------------------------------------------------------------   

#================= CLASE BASE =================
class Servicio(ABC):
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        if not isinstance(valor, int):
            raise ValueError("ID inválido: debe ser un número entero")

        if valor <= 0:
            raise ValueError("ID inválido: debe ser mayor a 0")

        self.__id = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nombre inválido")

        self.__nombre = valor.strip()

    def describir(self):
        return f"Servicio: {self.__nombre} (ID: {self.__id})"

    @abstractmethod
    def calcular_costos(self):
        pass

    @abstractmethod
    def calcular_descuento(self, cupon=False, cliente_premium=False):
        pass


#================= CLASES HIJAS =================
class ServicioSala(Servicio):
    def __init__(self, id, nombre, horas, tarifa_por_hora):
        super().__init__(id, nombre)
        self.horas = horas
        self.tarifa_por_hora = tarifa_por_hora

    @property
    def horas(self):
        return self.__horas

    @horas.setter
    def horas(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("Las horas deben ser numéricas")

        if valor <= 0:
            raise ValueError("Las horas deben ser mayores a 0")

        self.__horas = valor

    @property
    def tarifa_por_hora(self):
        return self.__tarifa_por_hora

    @tarifa_por_hora.setter
    def tarifa_por_hora(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("La tarifa debe ser numérica")

        if valor <= 0:
            raise ValueError("La tarifa debe ser mayor a 0")

        self.__tarifa_por_hora = valor

    def calcular_costos(self):
        return self.__horas * self.__tarifa_por_hora

    def calcular_descuento(self, cupon=False, cliente_premium=False):
        costo = self.calcular_costos()
        descuento = 0

        if cupon:
            descuento += costo * 0.05

        if cliente_premium:
            descuento += costo * 0.10

        return costo - descuento

    def describir(self):
        return (
            f"{super().describir()} | "
            f"Horas: {self.__horas} | "
            f"Tarifa: {self.__tarifa_por_hora} | "
            f"Total: {self.calcular_costos()}"
        )
        
  #-------------------------------------------------------------------
  #-----------------------Servicio de equipos-------------------------
  #-------------------------------------------------------------------      
class ServicioEquipo(Servicio):
    def __init__(self, id, nombre, tipo_equipo, dias, tarifa_dia, cantidad=1):
        super().__init__(id, nombre)
        
        self.__tipo_equipo = tipo_equipo
        self.dias = dias
        self.tarifa_dia = tarifa_dia
        self.cantidad = cantidad
        
    @property
    def tipo_equipo(self):
        return self.__tipo_equipo
        
    @property
    def dias(self):
        return self.__dias
        
    @dias.setter
    def dias(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("Días deben ser númericos")
            
        if valor <= 0:
            raise ValueError("Días deben ser mayores a 0")
            
        self.__dias = valor
            
    @property
    def tarifa_dia(self):
         return self.__tarifa_dia
        
    @tarifa_dia.setter
    def tarifa_dia(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("La tarifa debe ser numérica")
            
        if valor <= 0:
            raise ValueError("La tarifa debe ser mayor a 0")
            
        self.__tarifa_dia = valor
            
    @property
    def cantidad(self):
         return self.__cantidad
        
    @cantidad.setter
    def cantidad(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("La cantidad debe ser un entero")
            
        if valor <= 0:
            raise ValueError("Debe haber al menos 1 equipo")
            
        self.__cantidad = valor
            
    def calcular_costos(self):
        try:
            return self.__dias * self.__tarifa_dia * self.__cantidad

        except Exception as e:
            print("Error calculando costos:", e)
            return 0
        
    def calcular_descuento(self, cupon=False, cliente_premium=False):
        costo = self.calcular_costos()
        descuento = 0
            
        if cupon:
            descuento += costo * 0.10
                
        if cliente_premium:
            descuento += costo * 0.15
            
        return costo - descuento
        
    def describir(self):
         return (f"{super().describir()} |"
                f"Equipo: {self.__tipo_equipo} | "
                f"Dias: {self.__dias} |"
                f"Cantidad: {self.__cantidad} |"
                f"Total: {self.calcular_costos()}")

  #-------------------------------------------------------------------
  #-----------------------Asesorías especializadas--------------------
  #-------------------------------------------------------------------   
  
class ServicioAsesoria(Servicio):
    def __init__(self, id, nombre, tipo_asesoria, horas, tarifa_horas, nivel="básico"):
        super().__init__(id, nombre)
        
        self.__tipo_asesoria = tipo_asesoria
        self.horas = horas
        self.tarifa_horas = tarifa_horas
        self.__nivel = nivel
        
    @property
    def tipo_asesoria(self):
        return self.__tipo_asesoria
    
    @property
    def horas(self):
        return self.__horas
    
    @horas.setter
    def horas(self, valor):
         if not isinstance(valor, (int, float)):
            raise ValueError("Las horas deben ser númericas")
            
         if valor <= 0:
            raise ValueError("Las horas deben deben ser mayores a 0")
            
         self.__horas = valor
         
    @property
    def tarifa_horas(self):
        return self.__tarifa_horas
    
    @tarifa_horas.setter
    def tarifa_horas(self, valor):
         if not isinstance(valor, (int, float)):
            raise ValueError("Tarifas deben ser númericas")
            
         if valor <= 0:
            raise ValueError("Tarifas deben ser mayores a 0")
            
         self.__tarifa_horas = valor
         
    def calcular_costos(self):
        return self.__horas * self.__tarifa_horas
    
    def calcular_descuento(self, cupon=False, cliente_premium=False):
        costo = self.calcular_costos()
        descuento = 0
        
        if cupon:
            descuento += costo * 0.04
                
        if cliente_premium:
            descuento += costo * 0.12
            
        return costo - descuento
    
    def describir(self):
        return (f"{super().describir()} | "
                f"Tipo: {self.__tipo_asesoria} | "
                f"Horas: {self.__horas} | "
                f"Nivel: {self.__nivel} | "
                f"Total: {self.calcular_costos()}")
        
  #-------------------------------------------------------------------
  #-----------------------Clientes--------------------
  #-------------------------------------------------------------------   
class Cliente:
    def __init__(self, id, nombre, telefono, email, tipo="normal"):
        self.id = id
        self.__nombre = nombre
        self.telefono = telefono
        self.email = email
        self.tipo = tipo
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID inválido")
        
        self.__id = valor 
        
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def telefono(self):
        return self.__telefono
    
    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not valor.isdigit():
            raise ValueError("Teléfono debe contener solo números")
                
        self.__telefono = valor
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValueError("Email inválido")
        
        self.__email = valor
        
    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, valor):
        if valor not in ["normal", "premium"]:
            raise ValueError("Tipo debe ser normal o premium")
        
        self.__tipo = valor    
        
    def es_premium(self):
        return self.__tipo == "premium"
    
    def __str__(self):
        return f"Cliente: {self.__nombre} | ID: {self.__id} | Tipo: {self.__tipo}"
    
    
 #-------------------------------------------------------------------
  #-----------------------LOG-------------------
  #-------------------------------------------------------------------   
class Logger:
    
    FILE_PATH = "data/logs.txt"
    
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        
    def log(self, nivel, mensaje):
        tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{tiempo}] {nivel}: {mensaje}\n")
    
 #-------------------------------------------------------------------
  #-----------------------Manejo de datos de clientes-------------------
  #-------------------------------------------------------------------   
class ClienteDuplicadoError(Exception):
    pass


class RepositorioError(Exception):
    pass
    
class ClienteRepository:

    FILE_PATH = "data/clientes.json"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.logger = Logger()

        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                json.dump([], f)

    def get_clientes_registrados(self):
        try:
            with open(self.FILE_PATH, "r") as f:
                return json.load(f)

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

        finally:
            print("Operación de guardado finalizada")
    
            
#prueba en consola
repo = ClienteRepository()

try:
    cliente1 = Cliente(1, "Alda", "300123", "mail@gmail.com", "premium")

    repo.save_cliente(cliente1)

except ClienteDuplicadoError as e:
    print("DUPLICADO:", e)

except RepositorioError as e:
    print("ERROR REPOSITORIO:", e)

else:
    print("Cliente guardado correctamente ✔")

finally:
    print("Fin del proceso")