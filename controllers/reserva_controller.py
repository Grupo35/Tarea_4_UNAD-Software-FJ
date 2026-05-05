from tkinter import messagebox, simpledialog
from datetime import datetime


class ReservaController:

    def __init__(self, app, reserva, carrito, cl_repo, logger):
        self.app = app
        self.reserva = reserva
        self.carrito = carrito
        self.cl_repo = cl_repo
        self.logger = logger


#==============================================================================================
#===========================================Reservas creacion==================================
#==============================================================================================

    def crear_reserva(self):

        hoy = datetime.now().date()

        #validacion============================================

        #se verifica que haya objectos en el carritos
        if not self.carrito.servi_multi:
            messagebox.showwarning("Verificar", "El carrito está vacío")
            return

        #se pide la fecha de la reserva al usuario
        fecha = simpledialog.askstring(
            "Fecha",
            "Fecha de la reserva:",
            initialvalue=hoy,
            parent=self.app
        )

        #validaciones
        if not fecha:
            messagebox.showwarning("Verificar", "Debe ingresar una fecha")
            return

        try:
            fecha_valida = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return

        if fecha_valida.date() < hoy:
            messagebox.showerror("Error", "La fecha no puede ser pasada")
            
            self.logger.log(
                    "ERROR",
                    f"Creación de reserva fallida | fecha={fecha_valida} | motivo=fecha pasada"
                )
            return

        cliente = self.carrito.cliente_id

        # tomar la lista
        servicio = self.carrito.servi_multi

        total = self.carrito.total(
            cliente_premium=(self.carrito.tipo == "premium"),
            cupon=self.app.var_cupon.get()
        )

        try:
            reserva_crear = self.reserva.crear_reservas(
                cliente,
                servicio,
                fecha,
                total
            )

            messagebox.showinfo("Success", "Reserva creada")

            self.carrito.limpiar()

            self.app.carrito_controller.actualizar_carritoMulti()
            self.app.carrito_controller.calcular_total()

            self.app.show_cliente_reserva()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error inesperado")
            print(e)


#============================se cargan las reservas en tabla==============

    def cargar_reservas(self, filtro="todos"):

        self.app.tabla_reservas.delete(*self.app.tabla_reservas.get_children())

        clientes = self.cl_repo.get_clientes_registrados()
        mostrar_reservas = self.reserva.obtener_reservas()

        hay_datos = False

        for r in mostrar_reservas:

            if filtro != "todos" and r["estado"] != filtro:
                continue

            nombre_cliente = next(
                (c.nombre for c in clientes if c.id == r["cliente_id"]),
                "Desconocido"
            )

            self.app.tabla_reservas.insert(
                "",
                "end",
                values=(
                    r["id"],
                    nombre_cliente,
                    r["fecha"],
                    r["estado"]
                )
            )

            hay_datos = True

        #Mostrar y ocultar mensaje
        if not hay_datos:
            if filtro == "todos":
                mensaje = "No hay reservas registradas"
            else:
                mensaje = f"No hay reservas en estado: {filtro}"

            self.app.lbl_mensaje.config(text=mensaje)
            self.app.lbl_mensaje.pack()
        else:
            self.app.lbl_mensaje.pack_forget()


#================================================================================

    def reservas_dinamicas(self, event):

        filtro = self.app.estado_reserva_entry.get()

        mapa = {
            "Seleccione un estado": "todos",
            "Confirmadas": "confirmado",
            "Canceladas": "cancelado",
            "Pendientes": "pendiente"
        }

        filtro = mapa.get(filtro, "todos")

        self.cargar_reservas(filtro)


#=================Info reserva y cambio de estado============================================

    def info_reserva(self):

        seleccion = self.app.tabla_reservas.focus()

        if not seleccion:
            messagebox.showerror("Error", "Seleccione una reserva")
            return

        datos = self.app.tabla_reservas.item(seleccion, "values")

        self.app.show_info_reserva(datos)


#=====================================cambiar estado reserva========================================================

    def cambiar_estado(self):

        estado_seleccionado = self.app.estado_entry.get()

        estado_mapa = {
            "Confirmar": "confirmado",
            "Cancelar": "cancelado"
        }

        estado = estado_mapa.get(estado_seleccionado)

        if self.app.estado_actual == "cancelado":
            messagebox.showwarning("Atención", "No se puede modificar una reserva cancelada.")
            self.logger.log(
                "ERROR",
                f"Intento de modificación de reserva cancelada. RESERVA: {self.app.codigo_reserva}"
            )
            return

        if estado_seleccionado == "Seleccione un estado":
            messagebox.showerror("Error", "Seleccione un estado.")
            return

        if self.app.estado_actual == estado:
            messagebox.showwarning(
                "Atención",
                "La reserva ya se encuentra en ese estado."
            )
            
            self.logger.log(
                "ERROR",
                f"Intento de actualizar reserva sin cambios | RERSERVA: {self.app.codigo_reserva} | Estado: {self.app.estado_actual}"
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar cambio",
            f"¿Seguro que deseas cambiar el estado de la reserva a '{estado}'?"
        )

        if not respuesta:
            return

        self.reserva.cambiar_estado_reserva(self.app.codigo_reserva, estado)

        messagebox.showinfo("Success", "El estado de la reserva ha sido cambiado exitosamente")

        reservas = self.reserva.obtener_reservas()

        reserva_actual = next(
            (r for r in reservas if r["id"] == self.app.codigo_reserva),
            None
        )

        if reserva_actual:

            datos = (
                reserva_actual["id"],
                reserva_actual["cliente_id"],
                reserva_actual["fecha"],
                reserva_actual["estado"]
            )

            self.app.show_info_reserva(datos)