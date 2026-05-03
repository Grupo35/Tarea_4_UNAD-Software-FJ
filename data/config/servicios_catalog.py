#IMPORTACIONES
from models.servicios import Servicio, ServicioSala, ServicioEquipo, ServicioAsesoria

#servicios en lista
SERVICIOS = {
    1101: ServicioSala(1101, "Sala de Conferencias Principal", None, 50000),
    1102: ServicioSala(1102, "Sala Reuniones Pequeña", None, 40000),
    1103: ServicioSala(1103, "Sala VIP Ejecutiva", None, 100000),
    1104: ServicioSala(1104, "Sala Empresarial Plus", None, 120000),
    1105: ServicioSala(1105, "Sala Creativa Multimedia", None, 150000),
    2101: ServicioEquipo(2101, "Proyector Full HD", "Proyector", None, 50000, None),
    2102: ServicioEquipo(2102, "Sistema de Sonido Profesional", "Audio", None, 80000, None),
    2103: ServicioEquipo(2103, "Micrófonos Inalámbricos", "Audio", None, 20000, None),
    2104: ServicioEquipo(2104, "Pantalla LED 65 Pulgadas", "Pantalla", None, 90000, None),
    2105: ServicioEquipo(2105, "Laptop Empresarial", "Computo", None, 75000, None),
    3101: ServicioAsesoria(3101, "Asesoría en Programación", "Python / Software", None, 60000, "básico"),
    3102: ServicioAsesoria(3102, "Asesoría en Bases de Datos", "SQL / Modelado", None, 70000, "intermedio"),
    3103: ServicioAsesoria(3103, "Consultoría IA", "Inteligencia Artificial", None, 120000, "avanzado"),
    3104: ServicioAsesoria(3104, "Asesoría en Redes", "Infraestructura", None, 65000, "intermedio"),
    3105: ServicioAsesoria(3105, "Asesoría en Ciberseguridad", "Seguridad Informática", None, 110000, "avanzado")
}