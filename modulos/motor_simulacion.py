import random

class MotorSimulacion:
    def __init__(self):
        # Valores iniciales típicos de un separador en Mendoza
        self.presion = 115.0  # psi
        self.nivel = 14.2     # ft
        self.caudal = 450.0   # bpd

    def obtener_datos(self):
        # Simulamos pequeñas variaciones de instrumentos
        self.presion += random.uniform(-0.5, 0.5)
        self.nivel += random.uniform(-0.05, 0.05)
        self.caudal += random.uniform(-1.0, 1.0)
        
        return {
            "presion": round(self.presion, 2),
            "nivel": round(self.nivel, 2),
            "caudal": round(self.caudal, 2)
        }
