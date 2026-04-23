import random
import numpy as np

class MotorSimulacion:
# Dentro de la clase MotorSimulacion
def __init__(self):
    self.presion = 115.0
    self.nivel = 14.2
    self.caudal_base = 450.0
    self.historial = []
    self.esd_activo = False  # Estado de la planta

def obtener_datos(self):
    if self.esd_activo:
        # En ESD, la presión sube por el cierre y el caudal cae a cero
        self.presion = min(self.presion + 0.1, 160.0) 
        self.caudal_base = 0.0
    else:
        self.presion += random.uniform(-0.5, 0.5)
        self.caudal_base += random.uniform(-1.0, 1.0)
    
    return {
        "presion": round(self.presion, 2),
        "nivel": round(self.nivel, 2),
        "caudal": round(self.caudal_base, 2)
    }

def activar_esd(self):
    """Cierra las SDV (Válvulas de Seguridad)"""
    self.esd_activo = True
    self.caudal_base = 0.0

def reset_planta(self):
    """Normaliza la planta después de un ESD"""
    self.esd_activo = False
    self.presion = 115.0
    self.caudal_base = 450.0

    def evolucion_produccion(self):
        """Genera el array de datos que requiere el gráfico de scada.py"""
        # Si no hay historial, generamos una tendencia de las últimas 24 horas
        if not self.historial:
            self.historial = np.random.normal(self.caudal_base, 15, 24).tolist()
        else:
            # Agregamos el dato actual y mantenemos solo los últimos 24
            nuevo_dato = self.caudal_base + random.uniform(-5, 5)
            self.historial.append(nuevo_dato)
            if len(self.historial) > 24:
                self.historial.pop(0)
                
        return self.historial

    def simular_golpe_de_gas(self):
        """Simulación de evento inestable en separador"""
        self.presion += 20.0
        self.nivel -= 2.0
