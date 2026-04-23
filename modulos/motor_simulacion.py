import random
import numpy as np

class MotorSimulacion:
    def __init__(self):
        # Parámetros base para IPCL MENFA
        self.presion = 115.0  # psi
        self.nivel = 14.2     # ft
        self.caudal_base = 450.0 # bpd
        self.historial = [] # Para el gráfico del SCADA

    def obtener_datos(self):
        """Simula la fluctuación de instrumentos en tiempo real"""
        # Variaciones aleatorias normales
        self.presion += random.uniform(-0.5, 0.5)
        self.nivel += random.uniform(-0.05, 0.05)
        
        # El caudal puede verse afectado por factores externos en session_state
        self.caudal_base += random.uniform(-1.0, 1.0)
        
        return {
            "presion": round(self.presion, 2),
            "nivel": round(self.nivel, 2),
            "caudal": round(self.caudal_base, 2)
        }

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
