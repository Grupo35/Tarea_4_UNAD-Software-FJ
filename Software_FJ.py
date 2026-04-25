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
        return self.__dias * self.__tarifa_dia * self.__cantidad
        
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
  
class ServivioAsesoria(Servicio):
    def __init__(self, id, nombre, tipo_asesoria, horas, tarifa_horas, nivel="básico"):
        super().__init__(id, nombre)
        
        self.__tipo_asesoria = tipo_asesoria
        self.horas = horas
        self.tarifa_horas = tarifa_horas
        self._nivel = nivel
             
            
        
    
    
#test    
try:
    sala = ServicioSala(1101, "Sala 1", 2, 20000)

    print(sala.describir())
    print("Costo final:", sala.calcular_descuento())

except ValueError as e:
    print("ERROR CAPTURADO:", e)
    
#test 2

try:
    s = ServicioEquipo(1104, "Microfono", "Altavoces", 2, 25000, 2)
    
    print(s.describir())
    print("Costo total:", s.calcular_descuento())
    
except ValueError as t:
    print("Errores en entrada:", t)
