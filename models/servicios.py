 #importaciones importantes
 
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

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def calcular_costos(self):
        pass

    @abstractmethod
    def calcular_costo_final(self, cupon=False, cliente_premium=False):
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
        
        if valor is None:
            self.__horas = None #variable no difinida 
            return
        
        if valor is None or valor == "":
            raise ValueError("Las horas no pueden estar vacías")
            
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("Las horas deben ser un número válido")
        
        if valor <= 0:
            raise ValueError("Las horas deben ser mayores a 0")

        self.__horas = valor

    @property
    def tarifa_por_hora(self):
        return self.__tarifa_por_hora

    @tarifa_por_hora.setter
    def tarifa_por_hora(self, valor):
        if not isinstance(valor, (int)):
            raise ValueError("La tarifa debe ser numérica")

        if valor <= 0:
            raise ValueError("La tarifa debe ser mayor a 0")

        self.__tarifa_por_hora = valor

    def calcular_costos(self):
        return self.__horas * self.__tarifa_por_hora

    def calcular_costo_final(self, cupon=False, cliente_premium=False):
        costo = self.calcular_costos()
      
        if cupon:
            costo -= costo * 0.05
             # si tiene cupon se descuenta el porcentaje indicado

        if cliente_premium:
            costo += costo * 0.10
            #si es premium se monta un recargo
        
        return costo

        

    def describir(self):
        return (
            f"Horas: {self.horas}"
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
        
        if valor is None:
            self.__dias = None #variable no difinida 
            return
        
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
        if not isinstance(valor, (int)):
            raise ValueError("La tarifa debe ser numérica")
            
        if valor <= 0:
            raise ValueError("La tarifa debe ser mayor a 0")
            
        self.__tarifa_dia = valor
            
    @property
    def cantidad(self):
         return self.__cantidad
        
    @cantidad.setter
    def cantidad(self, valor):
        
        if valor is None:
            self.__cantidad = None #variable no difinida 
            return
        
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
        
    def calcular_costo_final(self, cupon=False, cliente_premium=False):
        costo = self.calcular_costos()
      
        if cupon:
            costo -= costo * 0.05
             # si tiene cupon se descuenta el porcentaje indicado

        if cliente_premium:
            costo += costo * 0.15
            #si es premium se monta un recargo
        
        return costo
        
    def describir(self):
         return (
                f"Dias: {self.__dias} |"
                f"Cantidad: {self.__cantidad} |"
         )

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
        
        if valor is None:
            self.__horas = None #variable no difinida 
            return
        
        if valor is None or valor == "":
            raise ValueError("Las horas no pueden estar vacías")
            
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("Las horas deben ser un número válido")
        
        if valor <= 0:
            raise ValueError("Las horas deben ser mayores a 0")

        self.__horas = valor
         
    @property
    def tarifa_horas(self):
        return self.__tarifa_horas
    
    @tarifa_horas.setter
    def tarifa_horas(self, valor):
         if not isinstance(valor, (int)):
            raise ValueError("Tarifas deben ser númericas")
            
         if valor <= 0:
            raise ValueError("Tarifas deben ser mayores a 0")
            
         self.__tarifa_horas = valor
         
    @property
    def nivel(self):
        return self.__nivel
         
    def calcular_costos(self):
        return self.__horas * self.__tarifa_horas
    
    def calcular_costo_final(self, cupon=False, cliente_premium=False):
        costo = self.calcular_costos()
      
        if cupon:
            costo -= costo * 0.10
             # si tiene cupon se descuenta el porcentaje indicado

        if cliente_premium:
            costo += costo * 0.15
            #si es premium se monta un recargo
        
        return costo
    
    def describir(self):
        return (
            f"Horas: {self.horas}"
        )
        