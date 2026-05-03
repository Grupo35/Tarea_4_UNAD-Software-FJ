from tkinter import messagebox
from models.servicios import ServicioSala, ServicioEquipo, ServicioAsesoria


class CarritoController:

    def __init__(self, app, carrito, servicios_catalog):
        self.app = app
        self.carrito = carrito
        self.servicios = servicios_catalog


    #============================= Agregar servicio al carrito multi==========================
    def agregar_al_carritoMulti(self):

        try:

            seleccion = self.app.tabla.selection()

            if not seleccion:
                messagebox.showerror("Error", "¡Seleccione un servicio de la lista!")
                return

            item = self.app.tabla.item(seleccion[0])
            id_servicio = int(item["values"][0])

            servicio_base = self.servicios.get(id_servicio)

            if not servicio_base:
                messagebox.showerror("Error", "Servicio no encontrado")
                return

            tipo = self.app.servicio_tipo_entry.get()

            # ================= SERVICIO SALA =================
            if tipo == "Servicio de Salas":

                if not hasattr(self.app, "hora_sa_entry"):
                    messagebox.showerror("Error", "Debe ingresar horas")
                    return

                hora = self.app.hora_sa_entry.get().strip()

                if not hora:
                    messagebox.showerror("Error", "El campo hora es obligatorio.")
                    return

                try:
                    hora = int(hora)
                except ValueError:
                    messagebox.showerror("Error", "Las horas deben ser numéricas.")
                    return

                servicio_nuevo = ServicioSala(
                    servicio_base.id,
                    servicio_base.nombre,
                    hora,
                    servicio_base.tarifa_por_hora
                )

                self.app.hora_sa_entry.delete(0, "end")

            # ================= SERVICIO EQUIPOS =================
            elif tipo == "Servicio de Equipos":

                if not hasattr(self.app, "dias_entry") or not hasattr(self.app, "cantidad_entry"):
                    messagebox.showerror("Error", "Debe ingresar días y cantidad")
                    return

                dias = self.app.dias_entry.get().strip()
                cantidad = self.app.cantidad_entry.get().strip()

                if not dias:
                    messagebox.showerror("Error", "El campo días es obligatorio.")
                    return

                if not cantidad:
                    messagebox.showerror("Error", "El campo cantidad es obligatorio.")
                    return

                try:
                    dias = int(dias)
                    cantidad = int(cantidad)
                except ValueError:
                    messagebox.showerror("Error", "Días y cantidad deben ser numéricos.")
                    return

                servicio_nuevo = ServicioEquipo(
                    servicio_base.id,
                    servicio_base.nombre,
                    servicio_base.tipo_equipo,
                    dias,
                    servicio_base.tarifa_dia,
                    cantidad
                )

                self.app.dias_entry.delete(0, "end")
                self.app.cantidad_entry.delete(0, "end")

            # ================= SERVICIO ASESORÍA =================
            elif tipo == "Servicio de Asesorias":

                if not hasattr(self.app, "hora_servicio_entry"):
                    messagebox.showerror("Error", "Debe ingresar horas")
                    return

                horas = self.app.hora_servicio_entry.get().strip()

                if not horas:
                    messagebox.showerror("Error", "El campo hora es obligatorio.")
                    return

                try:
                    horas = int(horas)
                except ValueError:
                    messagebox.showerror("Error", "Las horas deben ser numéricas.")
                    return

                servicio_nuevo = ServicioAsesoria(
                    servicio_base.id,
                    servicio_base.nombre,
                    servicio_base.tipo_asesoria,
                    horas,
                    servicio_base.tarifa_horas
                )

                self.app.hora_servicio_entry.delete(0, "end")

            else:
                messagebox.showerror("Error", "Seleccione un tipo de servicio válido")
                return

            # ================= AGREGAR AL CARRITO =================
            self.carrito.agregar_servicio(servicio_nuevo)

            self.actualizar_carritoMulti()
            self.calcular_total()

            messagebox.showinfo(
                "Carrito",
                f"{servicio_nuevo.nombre} añadido al carrito"
            )

            self.app.tabla.selection_remove(self.app.tabla.selection())
            self.app.tabla.focus("")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    #=======================actualizar info carrito==================
    def actualizar_carritoMulti(self):

        for fila in self.app.tabla_carrito.get_children():
            self.app.tabla_carrito.delete(fila)

        es_premium = (self.carrito.tipo == "premium")

        for s in self.carrito.servi_multi:

            self.app.tabla_carrito.insert(
                "",
                "end",
                values=(
                    s.id,
                    s.nombre,
                    s.describir(),
                    f"{s.calcular_costo_final(cliente_premium=es_premium):,.0f}".replace(",", ".")
                )
            )


    #============================calcular total e imprimir====================
    def calcular_total(self):

        es_premium = (self.carrito.tipo == "premium")

        total = self.carrito.total(
            cliente_premium=es_premium,
            cupon=self.app.var_cupon.get(),
        )

        self.app.total_var.set(f"Total: ${total:,.2f}")


    #=============limpieza============================
    def limpiar_carrito(self):

        self.carrito.limpiar()

        self.actualizar_carritoMulti()
        self.calcular_total()


    #===============funcion para dar atras============
    def dar_atras(self):

        self.limpiar_carrito()
        self.app.show_cliente_reserva()

        self.app.logger.log(
            "INFO",
            f"Cliente {self.carrito.cliente_id} ha cancelado la operación de reserva"
        )