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
    
    