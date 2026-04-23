# motor/motor_simulacion.py
import random
import time

class MotorSimulacion:
    def __init__(self):
        self.presion_separador = 120.0
        self.nivel_tanque = 14.2
        self.caudal_entrada = 450.0

    def obtener_datos_tiempo_real(self):
        """Simula la fluctuación de instrumentos de campo"""
        self.presion_separador += random.uniform(-0.5, 0.5)
        self.nivel_tanque += random.uniform(-0.1, 0.1)
        self.caudal_entrada += random.uniform(-2.0, 2.0)
        
        return {
            "presion": round(self.presion_separador, 2),
            "nivel": round(self.nivel_tanque, 2),
            "caudal": round(self.caudal_entrada, 2),
            "timestamp": time.strftime("%H:%M:%S")
        }

    def verificar_alarmas(self):
        """Lógica de control para alarmas de planta"""
        alertas = []
        if self.nivel_tanque > 15.0:
            alertas.append("⚠️ NIVEL ALTO EN TANQUE DE LAVADO (LAHH)")
        if self.presion_separador > 150.0:
            alertas.append("🛑 SOBREPRESIÓN EN SEPARADOR TRIDÁSICO")
        return alertas
