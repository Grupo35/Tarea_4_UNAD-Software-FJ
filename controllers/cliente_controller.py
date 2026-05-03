import tkinter as tk
from tkinter import messagebox
from models.cliente import Cliente
from repositories.cliente_repository import ClienteDuplicadoError


class ClienteController:

    def __init__(self, app):
        self.app = app  

    # ================= REGISTRAR CLIENTE =================
    def registrar_cliente(self):

        try:
            id_texto = self.app.id_entry.get().strip()
            nombre = self.app.nombre_entry.get().strip()
            telefono = self.app.telefono_entry.get().strip()
            email = self.app.email_entry.get().strip()
            tipo_ui = self.app.tipo_entry.get()

            tipos = {
                "Normal": "normal",
                "Premium": "premium"
            }

            tipo = tipos.get(tipo_ui)

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

            if tipo_ui == "Seleccione el tipo de cliente":
                messagebox.showerror("Error", "Seleccione un tipo de cliente.")
                return

            cliente = Cliente(
                int(id_texto),
                nombre,
                telefono,
                email,
                tipo
            )

            self.app.cl_repo.save_cliente(cliente)

            messagebox.showinfo("Success", "¡Cliente registrado con éxito!")

            self.limpiar_formulario()

        except ClienteDuplicadoError as e:
            messagebox.showerror("Error", str(e))

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ================= LIMPIAR =================
    def limpiar_formulario(self):
        self.app.id_entry.delete(0, tk.END)
        self.app.nombre_entry.delete(0, tk.END)
        self.app.telefono_entry.delete(0, tk.END)
        self.app.email_entry.delete(0, tk.END)
        self.app.tipo_entry.current(0)

    # ================= SELECCIONAR CLIENTE =================
    def seleccionar_cliente(self):

        seleccion = self.app.tabla_clientes.focus()

        if not seleccion:
            messagebox.showerror("Error", "Seleccione un cliente")
            return

        datos = self.app.tabla_clientes.item(seleccion, "values")

        self.app.carrito.cliente_id = int(datos[0])
        self.app.carrito.tipo = datos[2]

        self.app.show_servicios(datos)