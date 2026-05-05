#IMPORTACIONES IMPORTANTES

from models.servicios import Servicio, ServicioSala, ServicioEquipo, ServicioAsesoria
from utils.logger import Logger  
#==============================Carrito multiservicios========================================

class CarritoMulti:
    
    def __init__(self):
        
        #lista de servicios
        self.servi_multi = []
        
        self.logger = Logger()
        
        #self.cliente_id = None
        
    #agregar servicio
    def agregar_servicio(self, servicios):
        
        #SE VALIDA UNA SOLA SALA POR RESERVA
        if isinstance(servicios, ServicioSala):

            for s in self.servi_multi:

                if isinstance(s, ServicioSala):
                    self.logger.log(
                        "WARNING",
                        f"Cliente {self.cliente_id} intentó agregar más de una sala"
                    )
                    raise ValueError("Solo se permite una sala por reserva")
        
        self.servi_multi.append(servicios)
        self.logger.log(
            "INFO",
            f"Cliente {self.cliente_id} agregó {servicios.nombre} a su carrito"
        )
        
    #======================Calcular total==================================
    def total(self, cupon=False, cliente_premium=False):

        total = 0

        for s in self.servi_multi:

            precio_final = s.calcular_costo_final(cupon, cliente_premium)

            total += precio_final

        return total
    
    #=====================limpiar el carrito=============================
    
    def limpiar(self):
        
        self.servi_multi.clear()
        self.logger.log(
            "INFO",
            f"Cliente {self.cliente_id} ha formateado el carrito"
        )
