#IMPORTACIONES IMPORTANTES INTERFAZ
import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog

#IMPORTACION DE SERVICIOS
from repositories.cliente_repository import ClienteRepository
from services.carrito_multi import CarritoMulti
from utils.logger import Logger
from services.reserva_service import ReservaService
from models.cliente import Cliente
from repositories.cliente_repository import ClienteDuplicadoError
from models.servicios import Servicio, ServicioSala, ServicioEquipo, ServicioAsesoria
from data.config.servicios_catalog import SERVICIOS
from datetime import datetime
from controllers.carrito_controller import CarritoController
from controllers.reserva_controller import ReservaController

#---------------------Interfaz programa---------------------
class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Software FJ")
        self.geometry("850x900")
        self.resizable(False,False)
        
        #servicios iniciados
        self.cl_repo = ClienteRepository()
        
        #instancia del carritomulti
        self.carrito = CarritoMulti()
        
        self.logger = Logger() #inicio del logger
        
        self.reserva = ReservaService(self.cl_repo, self.logger)
        
        self.carrito_controller = CarritoController(self, self.carrito, SERVICIOS)
        
        self.reserva_controller = ReservaController(
            self,
            self.reserva,
            self.carrito,
            self.cl_repo,
            self.logger
        )
        
       
        
        self.show_home()#iniciamos la pantalla principal
        
        self.input_grupo = None 
        
      
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
        
        #==========================Tabla para mostrar reservas=================================
        self.frame_info = ttk.Frame(self)
        self.frame_info.pack(pady=10)
        self.frame_selector = ttk.Frame(self)
        self.frame_selector.pack(pady=5)
        # se crea el frame
        self.frame_reservas = tk.Frame(self)
        self.frame_reservas.pack()

        # se crea el label para mostrar el mensaje
        self.lbl_mensaje = tk.Label(self.frame_reservas, text="", fg="gray")
        self.lbl_mensaje.pack()
        self.lbl_mensaje.pack_forget()
        
        ttk.Label(
            self.frame_info,
            text="Reservas",
            font=("Arial", 16)
        ).pack(pady=5)
        
        self.estado_reserva_entry = self.lista_desplegable(
            self.frame_selector,
            "",
            0,
            0,
            [   
                "Seleccione un estado",
                "Pendientes",
                "Confirmadas",
                "Canceladas",
            ]
        )
        
        self.estado_reserva_entry.current(0)

        self.estado_reserva_entry.bind(
            "<<ComboboxSelected>>",
            self.reserva_controller.reservas_dinamicas
        )
        
        self.tabla_reservas = ttk.Treeview(
            self,
            columns=("codigo", "cliente", "fecha", "estado"),
            show="headings",
            height=10,
            selectmode="browse",
        )

        self.tabla_reservas.heading("codigo", text="Código")
        self.tabla_reservas.heading("cliente", text="Cliente")
        self.tabla_reservas.heading("fecha", text="Fecha")
        self.tabla_reservas.heading("estado", text="Estado")

        # ================= columnas =================
        self.tabla_reservas.column("codigo", width=80, anchor="center")
        self.tabla_reservas.column("cliente", width=150)
        self.tabla_reservas.column("fecha", width=80, anchor="center")
        self.tabla_reservas.column("estado", width=80, anchor="center")

        self.tabla_reservas.pack(pady=15)
        
        self.reserva_controller.cargar_reservas()
        
        #===========================================================================================
        
        #Botones agrupados de crear clientes y reserva
        
         #Botone de ver reservas 
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)
        ttk.Button(
            frame_botones,
            text="Ver más info",
            bootstyle="warning",
            command=self.reserva_controller.info_reserva,
        ).grid(row=0, column=0, padx=10)
        
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
        
#=========================================================================================================

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
        
#=====================================================================================

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
            selectmode="browse"  
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
        
        
#=================================================================================

#========================================Pantalla de reservas y servicios==========

    def show_servicios(self, datos):

        self.clear()

        # =====================================================
        #ubicacion de los frames en pantalla

        self.frame_info = ttk.Frame(self)
        self.frame_info.pack(pady=10)

        self.frame_selector = ttk.Frame(self)
        self.frame_selector.pack(pady=5)


        self.frame_tabla = ttk.Frame(self)
        self.frame_tabla.pack(pady=10)
        
        self.frame_inputs = ttk.Frame(self)
        self.frame_inputs.pack(pady=5)

        self.frame_carrito = ttk.Frame(self)
        self.frame_carrito.pack(pady=10, fill="x")


        ttk.Label(
            self.frame_info,
            text="Reservas",
            font=("Arial", 22)
        ).pack()

        ttk.Label(
            self.frame_info,
            text="Servicios",
            font=("Arial", 16)
        ).pack(pady=5)

        
        #datos del cliente
        
        id_cliente = datos[0]
        nombre = datos[1]
        tipo = datos[2]

        fila_cliente = ttk.Frame(self.frame_info)
        fila_cliente.pack(pady=5)

        ttk.Label(
            fila_cliente,
            text=f"ID: {id_cliente}"
        ).grid(row=0, column=0, padx=5)

        ttk.Label(
            fila_cliente,
            text=f"Nombre: {nombre}"
        ).grid(row=0, column=1, padx=5)

        ttk.Label(
            fila_cliente,
            text=f"Tipo: {tipo}"
        ).grid(row=0, column=2, padx=5)

        
        # =====================Lista de sevicio================================

        self.servicio_tipo_entry = self.lista_desplegable(
            self.frame_selector,
            "Servicios",
            0,
            0,
            [
                "Seleccione el tipo de servicios",
                "Servicio de Salas",
                "Servicio de Equipos",
                "Servicio de Asesorias"
            ]
        )

        self.servicio_tipo_entry.current(0)

        self.servicio_tipo_entry.bind(
            "<<ComboboxSelected>>",
            self.datos_dinamicos
        )

        
        #tabla servicios
        # =====================================================

        self.tabla = None
        self.mostrar_placeholder()


        #carrito servimulti
        # =====================================================

        ttk.Label(
            self.frame_carrito,
            text="Carrito de Servicios",
            font=("Arial", 14)
        ).pack(pady=5)

        columnas = ("id", "nombre", "detalle", "tarifa")

        self.tabla_carrito = ttk.Treeview(
            self.frame_carrito,
            columns=columnas,
            show="headings",
            height=8
        )

        for col in columnas:
            self.tabla_carrito.heading(col, text=col.upper())
            self.tabla_carrito.column(col, width=110, anchor="center")

        self.tabla_carrito.pack(fill="x", padx=10)
        
         #======================checkbox dde cupon======================
        # Variable de descuentos
        self.var_cupon = tk.BooleanVar()
        
        frame_check = ttk.Frame(self)
        frame_check.pack(pady=20)

        ttk.Checkbutton(
            frame_check,
            text="Aplicar cupón de descuento",
            variable=self.var_cupon,
            bootstyle="success",
            command=self.carrito_controller.calcular_total,
        ).grid(row=0, column=0, padx=10)
        
        
        #=================TOTAL==========================
        self.total_var = tk.StringVar(value="Total: $0.00")
        ttk.Label(
            self,
            textvariable=self.total_var,
            font=("Arial", 18),
            bootstyle="info",
        ).pack(pady=10)
        
        #SE IMPRIME EL TOTAL
        
        #botones de crear reserva y atrras
        
         
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)
        ttk.Button(
            frame_botones,
            text="Crear reserva",
            bootstyle="success",
            command=self.reserva_controller.crear_reserva,
        ).grid(row=0, column=0, padx=10)
        
        ttk.Button(
            frame_botones,
            text="Limpiar Carrito",
            bootstyle="warning",
            command=self.carrito_controller.limpiar_carrito,
            ).grid(row=0, column=1, padx=10)

        ttk.Button(
            frame_botones,
            text="Cancelar",
            bootstyle="danger",
            command=self.carrito_controller.dar_atras,
            ).grid(row=0, column=2, padx=10)

#==================================================================================================

#====================================Info reserva y cambio de estado==================================
    def show_info_reserva(self, datos):

        self.clear()
        
        clientes = self.cl_repo.get_clientes_registrados()

        self.frame_info = ttk.Frame(self)
        self.frame_info.pack(pady=10)
        

        ttk.Label(
            self.frame_info,
            text="Información de Reserva",
            font=("Arial", 22)
        ).pack(pady=10)

        id_reserva = datos[0]

        reservas = self.reserva.lista_reservas()

        reserva_dict = next(
            (r for r in reservas if r["id"] == id_reserva),
            None
        )

        #validacion de si existe o no la reserva
        if not reserva_dict:
            ttk.Label(
                self.frame_info,
                text="Reserva no encontrada",
                font=("Arial", 14)
            ).pack(pady=10)
            return

        #buscar info cliente para mostrar
        cliente_obj = next(
            (c for c in clientes if c.id == reserva_dict["cliente_id"]),
            None
        )

        if cliente_obj:
            nombre_cliente = cliente_obj.nombre
            telefonoCL = cliente_obj.telefono
            correoCL = cliente_obj.email
            tipoCL = cliente_obj.tipo
        else:
            nombre_cliente = "Desconocido"
            telefonoCL = "Desconocido"
            correoCL = "Desconocido"
            tipoCL = "Desconocido"

        # ================= INFO RESERVA =================
        info_reserva_frame = ttk.Frame(self.frame_info)
        info_reserva_frame.pack(pady=10)

        datos_reserva = [
            f"Código: {reserva_dict['id']}",
            f"Fecha: {reserva_dict['fecha']}",
            f"Total: ${reserva_dict['total']:,.0f}",
            f"Estado: {reserva_dict['estado']}"
        ]

        for i, texto in enumerate(datos_reserva):
            fila = i // 3
            columna = i % 3

            ttk.Label(
                info_reserva_frame,
                text=texto,
                font=("Arial", 14),
                padding=10
            ).grid(
                row=fila,
                column=columna,
                padx=15,
                pady=10,
                sticky="w"
            )

        #linea para separar
        ttk.Separator(self.frame_info, orient="horizontal").pack(fill="x", pady=15)

        # ================= infotmacion cliente =================
        ttk.Label(
            self.frame_info,
            text="Información del Cliente",
            font=("Arial", 18)
        ).pack(pady=5)

        info_cliente_frame = ttk.Frame(self.frame_info)
        info_cliente_frame.pack(pady=10)

        datos_cliente = [
            f"ID: {reserva_dict['cliente_id']}",
            f"Nombre: {nombre_cliente}",
            f"Teléfono: {telefonoCL}",
            f"Correo: {correoCL}",
            f"Tipo: {tipoCL}"
        ]

        for i, texto in enumerate(datos_cliente):

            fila = i // 2
            columna = i % 2

            ttk.Label(
                info_cliente_frame,
                text=texto,
                font=("Arial", 12),
                padding=2
            ).grid(
                row=fila,
                column=columna,
                padx=5,
                pady=2,
                sticky="w"
            )
            
        ttk.Separator(self.frame_info, orient="horizontal").pack(fill="x", pady=15)
        
        #info servicios==============================================================
        
         # ================= infotmacion cliente =================
        ttk.Label(
            self.frame_info,
            text="Servicios Contratados",
            font=("Arial", 18)
        ).pack(pady=5)
        
        self.tabla_servicios_contratados = ttk.Treeview(
        self,
        columns=("id", "nombre", "detalle", "tarifa"),  
        show="headings",
        height=10,
        )

        self.tabla_servicios_contratados.heading("id", text="ID")
        self.tabla_servicios_contratados.heading("nombre", text="Nombre Servicio")
        self.tabla_servicios_contratados.heading("detalle", text="Detalles")
        self.tabla_servicios_contratados.heading("tarifa", text="Tarifa")

    # ================= columnas =================
        self.tabla_servicios_contratados.column("id", width=80, anchor="center")
        self.tabla_servicios_contratados.column("nombre", width=200, anchor="center")
        self.tabla_servicios_contratados.column("detalle", width=150, anchor="center")
        self.tabla_servicios_contratados.column("tarifa", width=80, anchor="center")

        self.tabla_servicios_contratados.pack(pady=15)
        self.tabla_servicios_contratados.delete(*self.tabla_servicios_contratados.get_children())
        
        if reserva_dict:

            servicios = reserva_dict.get("servicios", [])

            for servicio in servicios:

                #descripción (duración + detalles)
                if servicio.get("_ServicioSala__horas"):
                    descripcion = f"{servicio.get('_ServicioSala__horas')} horas"

                elif servicio.get("_ServicioEquipo__dias"):
                    descripcion = (
                        f"{servicio.get('_ServicioEquipo__dias')} días - "
                        f"{servicio.get('_ServicioEquipo__tipo_equipo')} "
                        f"(x{servicio.get('_ServicioEquipo__cantidad')})"
                    )

                elif servicio.get("_ServicioAsesoria__horas"):
                    descripcion = (
                        f"{servicio.get('_ServicioAsesoria__horas')} horas - "
                        f"{servicio.get('_ServicioAsesoria__nivel')}"
                    )

                else:
                    descripcion = "N/A"

                #tarifa
                tarifa = (
                    servicio.get("_ServicioSala__tarifa_por_hora")
                    or servicio.get("_ServicioEquipo__tarifa_dia")
                    or servicio.get("_ServicioAsesoria__tarifa_horas")
                )

                self.tabla_servicios_contratados.insert(
                    "",
                    "end",
                    values=(
                        servicio.get("_Servicio__id"),
                        servicio.get("_Servicio__nombre"),
                        descripcion,
                        tarifa if tarifa is not None else "N/A"
                    )
                )
                
            # =====================Lista de de estados================================
            
        self.frame_selector = ttk.Frame(self)
        self.frame_selector.pack(pady=5)
        self.codigo_reserva = reserva_dict['id']
        self.estado_actual = reserva_dict['estado']#estado actual 
        
        self.estado_entry = self.lista_desplegable(
            self.frame_selector,
            "Estado:",
            0,
            0,
            [
                "Seleccione un estado",
                "Confirmar",
                "Cancelar"
            ]
        )

        
        #==============================botonces de accion=======================================
        frame_botones = ttk.Frame(self)
        frame_botones.pack(pady=10)
        ttk.Button(
            frame_botones,
            text="Actualizar Estado",
            bootstyle="success",
            command=self.reserva_controller.cambiar_estado,
        ).grid(row=0, column=0, padx=10)
        
        ttk.Button(
            frame_botones,
            text="Atrás",
            bootstyle="warning",
            command=self.show_home,
            ).grid(row=0, column=1, padx=10)


#==========================================================================================       
#====================================Acciones==============================================
#==========================================================================================

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
        
         # guardar cliente en el carrito
        self.carrito.cliente_id = int(datos[0])
        self.carrito.tipo = (datos[2])
        
        # pasar a otra función
        self.show_servicios(datos)
        
#Combinacion dinamica select + tabla

    def datos_dinamicos(self, event):
        
        datos = self.servicio_tipo_entry.get()
        self.limpiar_tabla()
        
        # Limpiar inputs también aquí
        if hasattr(self, "input_grupo") and self.input_grupo:
            try:
                if self.input_grupo.winfo_exists():
                    self.input_grupo.destroy()
            except:
                pass
            self.input_grupo = None
            
        #limpiar botones al regresar al estado original
        if hasattr(self, "frame_botones") and self.frame_botones:
            try:
                if self.frame_botones.winfo_exists():
                    self.frame_botones.destroy()
            except:
                pass
            self.frame_botones = None
        
        if datos == "Seleccione el tipo de servicios":
            self.mostrar_placeholder()
            return
        
        elif datos == "Servicio de Salas":
            
            columnas = ("codigo", "nombre", "tarifa")
            encabezados = ("Código", "Nombre", "tarifa")
            
            
        elif datos == "Servicio de Equipos":
            columnas = ("codigo", "nombre", "tipo", "tarifa")
            encabezados = ("Código", "Nombre", "Tipo", "Tarifa")
            #id, nombre, tipo_equipo, dias, tarifa_dia, cantidad=1
            
        elif datos == "Servicio de Asesorias":
            columnas = ("codigo", "nombre", "tarifa", "nivel")
            encabezados = ("Código", "Nombre", "Tarifa", "Nivel")
            
            #self, id, nombre, tipo_asesoria, horas, tarifa_horas, nivel="básico"
        
        else:
            self.mostrar_placeholder()
            return
              
        self.construir_tabla(columnas, encabezados)
        self.datos_tabla(datos)
        self.input_dinamicos(datos)
        
        
            
  # Contruccion y destruccion de tabla
            
    def construir_tabla(self, columnas, encabezados):

        # destruir tabla anterior
        if self.tabla:
            self.tabla.destroy()

        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=columnas,
            show="headings",
            height=6,
            selectmode="browse"
        )

        for col, titulo in zip(columnas, encabezados):

            # encabezado
            self.tabla.heading(col, text=titulo, anchor="center")

            # configuración dinámica de columnas
            if col == "id" or col == "codigo":
                self.tabla.column(
                    col,
                    width=80,
                    anchor="center"
                )

            elif col == "nombre":
                self.tabla.column(
                    col,
                    width=180,
                    anchor="w"
                )

            elif col == "tipo":
                self.tabla.column(
                    col,
                    width=80,
                    anchor="center"
                )

            elif col == "nivel":
                self.tabla.column(
                    col,
                    width=120,
                    anchor="center"
                )

            elif col == "tarifa":
                self.tabla.column(
                    col,
                    width=80,
                    anchor="center"
                )

            elif col == "cantidad":
                self.tabla.column(
                    col,
                    width=100,
                    anchor="center"
                )

            elif col == "dias":
                self.tabla.column(
                    col,
                    width=100,
                    anchor="center"
                )

            elif col == "horas":
                self.tabla.column(
                    col,
                    width=100,
                    anchor="center"
                )

            elif col == "area":
                self.tabla.column(
                    col,
                    width=180,
                    anchor="center"
                )

            else:
                self.tabla.column(
                    col,
                    width=150,
                    anchor="center"
                )

        self.tabla.pack(pady=10)     
        
        
        # ================= LIMPIAR =================
    def limpiar_tabla(self):

        # borrar tabla si existe
        if self.tabla:
            self.tabla.destroy()
            self.tabla = None
            
         # borrar placeholder e
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()
            
    def mostrar_placeholder(self):

        self.limpiar_tabla()

        columnas = ("mensaje",)
        encabezados = ("Estado",)

        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=columnas,
            show="headings",
            height=3
        )

        self.tabla.heading("mensaje", text="Estado")
        self.tabla.column("mensaje", anchor="center", width=300)

        self.tabla.pack(pady=10)

        self.tabla.insert(
            "",
            "end",
            values=("No hay datos. Seleccione un servicio",)
        )
        
    #================Constuir inputs=========================
    def input_dinamicos(self, datos):

        
        #limpiar contenido
        # ==================================================
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()

        if datos == "Seleccione el tipo de servicios":
            return

    
        #contendor
        # ==================================================
        self.input_grupo = ttk.Frame(self.frame_inputs)
        self.input_grupo.pack(pady=5)

        # ================= sala =================
        if datos == "Servicio de Salas":

            self.hora_sa_entry = self.create_input(
                self.input_grupo,
                "Horas a alquilar:",
                0,
                0
            )

        # ================= equipos =================
        elif datos == "Servicio de Equipos":

            self.dias_entry = self.create_input(
                self.input_grupo,
                "Días a alquilar",
                0,
                0
            )

            self.cantidad_entry = self.create_input(
                self.input_grupo,
                "Cantidad de equipos:",
                0,
                1
            )

        # ================= asesoria =================
        elif datos == "Servicio de Asesorias":

            self.hora_servicio_entry = self.create_input(
                self.input_grupo,
                "Horas",
                0,
                0
            )

        #botones dinamicos
        # ==================================================
        self.frame_botones = ttk.Frame(self.frame_inputs)
        self.frame_botones.pack(pady=5)

        ttk.Button(
            self.frame_botones,
            text="Agregar",
            bootstyle="warning",
            command=self.carrito_controller.agregar_al_carritoMulti
        ).grid(row=0, column=0, padx=10)
        
            
#=================================Llenar tabla=========================
    def datos_tabla(self, datos):
         # Limpiar datos existentes
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        if datos == "Servicio de Salas":
            
            servi_salas = [
                s for s in SERVICIOS.values()
                if isinstance(s, ServicioSala)
            ]
            
            for servicio in servi_salas:
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        servicio.id,
                        servicio.nombre,
                        servicio.tarifa_por_hora
                    )
                )
                
        elif datos == "Servicio de Equipos":
            
            servi_salas = [
                s for s in SERVICIOS.values()
                if isinstance(s, ServicioEquipo)
            ]
            
            for servicio in servi_salas:
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        servicio.id,
                        servicio.nombre,
                        servicio.tipo_equipo,
                        servicio.tarifa_dia
                    )
                )
                
        elif datos == "Servicio de Asesorias":
            
            servi_salas = [
                s for s in SERVICIOS.values()
                if isinstance(s, ServicioAsesoria)
            ]
            
            for servicio in servi_salas:
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        servicio.id,
                        servicio.nombre,
                        servicio.tarifa_horas,
                        servicio.nivel
                    )
                )
            
 

