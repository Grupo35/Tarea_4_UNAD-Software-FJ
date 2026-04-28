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

        
    
            
 #-------------------------------------------------------------------
  #-----------------------Reservas-------------------
  #-------------------------------------------------------------------   
  
class Reserva:
    def __init__(self, id, cliente, servicio, fecha):
        self.id = id
        self.cliente = cliente
        self.servicio = servicio
        self.fecha = fecha
        self.estado = "pendiente"

    # ---------------- ID ----------------
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        if not isinstance(valor, int):
            raise ValueError("ID inválido: debe ser entero")
        if valor <= 0:
            raise ValueError("ID inválido: debe ser mayor a 0")
        self.__id = valor

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

    def obtener_total(self, cliente_premium=False):
        costo = self.servicio.calcular_costos()

        if cliente_premium:
            costo = self.servicio.calcular_descuento(cliente_premium=True)

        return costo

    def describir(self):
        return (
            f"Reserva ID: {self.__id} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Fecha: {self.fecha} | "
            f"Estado: {self.estado} | "
            f"Total: {self.obtener_total(self.cliente.es_premium())}"
        )
        
# ===================== RESERVA SERVICE =====================
class ReservaService:

    FILE_PATH = "data/reservas.json"

    def __init__(self, cliente_repo, logger):
        self.cliente_repo = cliente_repo
        self.logger = logger
        self.reservas = []

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                json.dump([], f)

    # ---------------- LISTAR RESERVAS ----------------
    def lista_reservas(self):
        with open(self.FILE_PATH, "r") as f:
            return json.load(f)

    # ---------------- VALIDAR DUPLICADOS ----------------
    def es_reserva_duplicada(self, id_cliente, servicio_nombre, fecha):

        reservas_json = self.lista_reservas()

        for r in reservas_json:
            if (
                r["cliente_id"] == id_cliente and
                r["servicio"] == servicio_nombre and
                r["fecha"] == str(fecha)
            ):
                return True

        for r in self.reservas:
            if (
                r.cliente.id == id_cliente and
                r.servicio.nombre == servicio_nombre and
                str(r.fecha) == str(fecha)
            ):
                return True

        return False

    # ---------------- CREAR RESERVA ----------------
    def crear_reservas(self, id_reserva, id_cliente, servicio, fecha):

        try:
            # ---------------- VALIDAR SERVICIO ----------------
            servicio_obj = SERVICIOS.get(servicio)

            if not servicio_obj:
                self.logger.log("ERROR", f"Servicio no existe ID {servicio}")
                raise ValueError("El servicio no existe")

            # ---------------- VALIDAR DUPLICADO ----------------
            if self.es_reserva_duplicada(id_cliente, servicio_obj.nombre, fecha):
                self.logger.log(
                    "ERROR",
                    f"Reserva duplicada cliente:{id_cliente} servicio:{servicio_obj.nombre} fecha:{fecha}"
                )
                raise ValueError("Ya existe una reserva con estos datos")

            # ---------------- BUSCAR CLIENTE ----------------
            clientes = self.cliente_repo.get_clientes_registrados()

            cliente_data = next(
                (c for c in clientes if c["id"] == id_cliente),
                None
            )

            if not cliente_data:
                self.logger.log("ERROR", f"Cliente no registrado {id_cliente}")
                raise ValueError("Cliente no registrado")

            # ---------------- CREAR CLIENTE ----------------
            cliente = Cliente(
                cliente_data["id"],
                cliente_data["nombre"],
                cliente_data["telefono"],
                cliente_data["email"],
                cliente_data["tipo"]
            )

            # ---------------- crear reserva ----------------
            reserva = Reserva(id_reserva, cliente, servicio_obj, fecha)

            # ---------------- guardado en memoria ----------------
            self.reservas.append(reserva)

            # ---------------- guardar en json ----------------
            self.guardar_json(reserva)

            self.logger.log("INFO", f"Reserva creada ID {id_reserva}")

            return reserva

        except Exception as e:
            self.logger.log("ERROR", str(e))
            raise

    # ---------------- Guardar ----------------
    def guardar_json(self, reserva):

        with open(self.FILE_PATH, "r") as f:
            data = json.load(f)

        data.append({
            "id": reserva.id,
            "cliente_id": reserva.cliente.id,
            "servicio": reserva.servicio.nombre,
            "fecha": str(reserva.fecha),
            "estado": reserva.estado,
            "total": reserva.obtener_total(reserva.cliente.es_premium())
        })

        with open(self.FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    # ---------------- CAMBIAR ESTADO ----------------
    def cambiar_estado(self, reserva, estado):

        try:
            reserva.estado = estado
            self.logger.log("INFO", f"Estado cambiado a {estado}")

        except Exception as e:
            self.logger.log("ERROR", str(e))
            raise
        
#servicios en lista
SERVICIOS = {
    1: ServicioSala(1, "Sala de Conferencias Principal", 1, 25000),
    2: ServicioSala(2, "Sala Reuniones Pequeña", 1, 18000),
    3: ServicioEquipo(3, "Proyector Full HD", "Proyector", 1, 50000, 1),
    4: ServicioEquipo(4, "Sistema de Sonido", "Audio Profesional", 1, 80000, 1),
    5: ServicioEquipo(5, "Micrófonos inalámbricos", "Audio", 1, 20000, 1),
    6: ServicioAsesoria(6, "Asesoría en Programación", "Python / Software", 1, 60000, "básico"),
    7: ServicioAsesoria(7, "Asesoría en Bases de Datos", "SQL / Modelado", 1, 70000, "intermedio"),
    8: ServicioAsesoria(8, "Consultoría Avanzada IA", "Inteligencia Artificial", 1, 120000, "avanzado")
}
    
    
#---------------------Interfaz programa---------------------
class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Software FJ")
        self.geometry("500x400")
        self.resizable(False,False)
        
        #servicios iniciados
        self.cl_repo = ClienteRepository()
        
        self.show_home()#iniciamos la pantalla principal
        
        
    #limpiar ventana    
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()
            
    def create_input(self, parent, label, row, column, show=None, placeholder=None):

        campo = ttk.Frame(parent)
        campo.grid(row=row, column=column, padx=15, pady=10, sticky="w")

        ttk.Label(campo, text=label).pack(anchor="w")

        entry = ttk.Entry(campo, width=30, show=show)
        entry.pack()

        # placeholder
        if placeholder:

            entry.insert(0, placeholder)
            entry.config(foreground="gray")

            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(foreground="white")

            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(foreground="gray")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)

        return entry
    
    #input select-------------------------------------------------------------------
    def lista_desplegable(self, parent, label, row, column, opciones, default=0):

        campo = ttk.Frame(parent)
        campo.grid(row=row, column=column, padx=15, pady=10, sticky="w")

        ttk.Label(campo, text=label).pack(anchor="w")

        combo = ttk.Combobox(
            campo,
            width=28,
            values=opciones,
            state="readonly"
        )
        combo.pack()

        if opciones:
            combo.current(default)

        return combo
    
    #pantalla principal-------------------------------------------------------------------
    def show_home(self):
        self.clear()
        
        ttk.Label(self, text = "Bienvenido", font = ("Arial", 24)).pack(pady = 25)
        
        #Botones agrupados de crear clientes y reserva
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)
        ttk.Button(
            frame_botones,
            text="Registrar Cliente",
            bootstyle="success",
            command=self.show_clientes,
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            frame_botones,
            text="Registrar Reserva",
            bootstyle="success",
            command=self.show_cliente_reserva,
        ).grid(row=0, column=1, padx=10)
        
        #Botone de ver reservas 
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)
        ttk.Button(
            frame_botones,
            text="Reservas Creadas",
            bootstyle="warning",
            command=self.clear,
        ).grid(row=0, column=0, padx=10)
        
#Pantalla de creacion de usuarios###########################################################
    def show_clientes(self):
        self.clear()

        ttk.Label(
            self,
            text="Registrar Cliente",
            font=("Arial", 24)
        ).pack(pady=25)

        input_grupo = ttk.Frame(self)
        input_grupo.pack(pady=10)

        # fila 0
        self.id_entry = self.create_input(input_grupo, "ID Cliente", 0, 0)
        self.nombre_entry = self.create_input(input_grupo, "Nombre del Cliente", 0, 1)

        # fila 1
        self.telefono_entry = self.create_input(input_grupo, "Teléfono", 1, 0)
        self.email_entry = self.create_input(input_grupo, "Email", 1, 1)

        # fila 2
        self.tipo_entry = self.lista_desplegable(
            input_grupo,
            "Tipo Cliente",
            2,
            0,
            ["Seleccione el tipo de cliente","Normal", "Premium"]
        )
        
        #botones de accion
        #Botones agrupados de crear clientes y reserva
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)
        ttk.Button(
            frame_botones,
            text="Registrar",
            bootstyle="success",
            command=self.registrar_cliente,
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            frame_botones,
            text="Atrás",
            bootstyle="danger",
            command=self.show_home,
        ).grid(row=0, column=1, padx=10)
        
#=================================Pantalla de escoger usuario para reserva======================
    def show_cliente_reserva(self):

        self.clear()

        # contenedor principal
        contenedor = ttk.Frame(self)
        contenedor.pack(pady=20)

        ttk.Label(
            contenedor,
            text="Reservas",
            font=("Arial", 22)
        ).pack(pady=10)

        ttk.Label(
            contenedor,
            text="Escoger cliente",
            font=("Arial", 16)
        ).pack(pady=5)
        
        self.tabla_clientes = ttk.Treeview(
            self,
            columns=("id", "nombre", "tipo"),
            show="headings",
            height=2,
            selectmode="browse"  # 👈 SOLO UNA FILA
        )
        
        self.tabla_clientes = ttk.Treeview(
            self,
            columns=("id", "nombre", "tipo"),
            show="headings",
            height=10,
        )

        self.tabla_clientes.heading("id", text="ID")
        self.tabla_clientes.heading("nombre", text="Nombre")
        self.tabla_clientes.heading("tipo", text="Tipo")

        # ================= columnas =================
        self.tabla_clientes.column("id", width=80, anchor="center")
        self.tabla_clientes.column("nombre", width=150)
        self.tabla_clientes.column("tipo", width=80, anchor="center")

        self.tabla_clientes.pack(pady=15)

        clientes = self.cl_repo.get_clientes_registrados()

        for cliente in clientes:
            self.tabla_clientes.insert(
                "",
                "end",
                values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.tipo
                )
            )
            
        #Botones agrupados de crear clientes y reserva
            frame_botones = ttk.Frame(self)
            frame_botones.pack(pady=10)
            ttk.Button(
                frame_botones,
                text="Seleccionar",
                bootstyle="success",
                command=self.seleccionar_cl,
            ).grid(row=0, column=0, padx=10)

            ttk.Button(
                frame_botones,
                text="Atrás",
                bootstyle="danger",
                command=self.show_home,
            ).grid(row=0, column=1, padx=10)
            
#========================================Pantalla de reservas y servicios==========

    def show_servicios(self, datos):

        self.clear()

        # contenedor principal
        contenedor = ttk.Frame(self)
        contenedor.pack(pady=20)

        ttk.Label(
            contenedor,
            text="Reservas",
            font=("Arial", 22)
        ).pack(pady=10)

        ttk.Label(
            contenedor,
            text="Servicios",
            font=("Arial", 16)
        ).pack(pady=5)

        # ================= datos del cliente =================

        id_cliente = datos[0]
        nombre = datos[1]
        tipo = datos[2]

        frame_cliente = ttk.Frame(contenedor)
        frame_cliente.pack(pady=10)

        ttk.Label(
            frame_cliente,
            text=f"ID Cliente: {id_cliente}",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10)

        ttk.Label(
            frame_cliente,
            text=f"Nombre: {nombre}",
            font=("Arial", 12)
        ).grid(row=0, column=1, padx=10)

        ttk.Label(
            frame_cliente,
            text=f"Tipo: {tipo}",
            font=("Arial", 12)
        ).grid(row=0, column=2, padx=10)
        
        
        
        
        
        
        
        
        
#====================================Acciones==============================================

#Registrar clientes

    def registrar_cliente(self):

        try:
            id_texto = self.id_entry.get().strip()
            nombre = self.nombre_entry.get().strip()
            telefono = self.telefono_entry.get().strip()
            email = self.email_entry.get().strip()
            tipo_ui = self.tipo_entry.get()

            tipos = {
                "Normal": "normal",
                "Premium": "premium"
            }

            tipo = tipos.get(tipo_ui)

            # ==================== ALIDACIONES====================

            if not id_texto:
                messagebox.showerror("Error", "El campo ID es obligatorio.")
                return

            if not id_texto.isdigit():
                messagebox.showerror("Error", "El ID debe ser numérico.")
                return

            if not nombre:
                messagebox.showerror("Error", "El campo Nombre es obligatorio.")
                return

            if not telefono:
                messagebox.showerror("Error", "El campo Teléfono es obligatorio.")
                return

            if not email:
                messagebox.showerror("Error", "El campo Email es obligatorio.")
                return

            if tipo == "Seleccione el tipo de cliente":
                messagebox.showerror("Error", "Seleccione un tipo de cliente.")
                return

            #convertir después de validar
            id = int(id_texto)

            cl = Cliente(id, nombre, telefono, email, tipo)

            self.cl_repo.save_cliente(cl)

            messagebox.showinfo("Success", "¡Cliente registrado con éxito!")
            
            self.id_entry.delete(0, tk.END)
            self.nombre_entry.delete(0, tk.END)
            self.telefono_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.tipo_entry.current(0)
            

        except ClienteDuplicadoError as e:
            messagebox.showerror("Error", str(e))

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            

#===============================seleccionar clientes de la tabla para extraer datos========
            
    def seleccionar_cl(self):

        seleccion = self.tabla_clientes.focus()

        if not seleccion:
            messagebox.showerror("Error", "Seleccione un cliente")
            return

        datos = self.tabla_clientes.item(seleccion, "values")
        
        # pasar a otra función
        self.show_servicios(datos)
        
         
            
            
# ================================= EJECUCION PROGRAMA ==========================================
if __name__ == "__main__":
    app = App()
    app.mainloop()