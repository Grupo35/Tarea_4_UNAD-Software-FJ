# Tarea_4_UNAD-Software-FJ
Tarea # 4 de programación: Componente práctico - Prácticas simuladas

# Sistema de Reservas Multiservicios
Descripción:

Este proyecto es una aplicación desarrollada en Python orientada a la gestión de reservas de servicios múltiples. El sistema permite administrar clientes, seleccionar servicios, agregarlos a un carrito temporal y calcular costos finales según las condiciones del cliente.

La aplicación fue desarrollada utilizando programación orientada a objetos (POO) y una interfaz gráfica construida con Tkinter y ttkbootstrap.

# Características principales
Gestión de clientes.
Gestión de servicios.
Carrito temporal de reservas.
Selección dinámica de servicios.
Validaciones de entradas.
Cálculo automático de costos.
Aplicación de recargos para clientes premium.
Aplicación de cupones de descuento.
Registro de eventos mediante logs.
Restricción de una sola sala por reserva.
Interfaz gráfica dinámica.

# Tecnologías utilizadas
Python 3
Tkinter
ttkbootstrap
Programación Orientada a Objetos (POO)

# Estructura del proyecto

APP/
│
├── controllers/
├── data/
├── models/
├── repositories/
├── services
├── utils/
├── views
├── .gitignore
├── README.md
└── Software_FJ.py

# Clases principales

CarritoMulti

Clase encargada de administrar los servicios agregados temporalmente a una reserva.

Funciones principales
Agregar servicios.
Calcular total.
Limpiar carrito.
Registrar acciones mediante logs.
Validar reglas de negocio.

ServicioSala

Representa los servicios de alquiler de salas.

Características
Manejo de horas.
Tarifa por hora.
Cálculo de costos.

ServicioEquipo

Representa servicios relacionados con alquiler de equipos.

Características
Manejo de días.
Manejo de cantidad.
Tarifa diaria.

ServicioAsesoria

Representa servicios de asesorías.

Características
Manejo de horas.
Tarifas por asesoría.

# Reglas de negocio

El sistema implementa diferentes reglas para controlar el flujo de reservas:

Solo se permite una sala por reserva.
Los equipos pueden agregarse múltiples veces.
Las asesorías pueden agregarse múltiples veces.
Los clientes premium reciben un recargo adicional.
Los cupones generan descuentos automáticos.

# Funcionamiento general

El usuario selecciona un cliente.
El sistema identifica si el cliente es normal o premium.
El usuario selecciona un tipo de servicio.
Se generan inputs dinámicos según el servicio.
El servicio se agrega al carrito.
El sistema calcula automáticamente el costo final.
El usuario puede limpiar o cancelar la operación.


# Validaciones implementadas

El sistema valida:

Campos vacíos.
Datos numéricos.
Horas válidas.
Días válidos.
Cantidades válidas.
Existencia de servicios.
Selección de elementos en tablas.

# Programación Orientada a Objetos aplicada

En el proyecto se aplican conceptos de:

Encapsulamiento.
Herencia.
Polimorfismo.
Sobrescritura de métodos.
Uso de setters y getters.
Modularidad.

# Interfaz gráfica

La interfaz fue desarrollada con Tkinter y ttkbootstrap.

Características:

Tablas dinámicas.
Formularios dinámicos.
Botones interactivos.
Mensajes de validación.
Actualización automática del carrito.

# Ejecución del proyecto

Requisitos

Instalar Python 3.

Instalar ttkbootstrap

# Ejecutar el sistema

python Software_FJ.py

# Ejemplo de uso

Seleccionar un cliente.
Elegir un servicio.
Ingresar los datos solicitados.
Agregar al carrito.
Verificar el total.
Crear la reserva.

# Autores

Proyecto desarrollado por los estudiante como práctica de programación orientada a objetos y desarrollo de interfaces gráficas en Python.