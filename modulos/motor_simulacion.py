import random
import numpy as np

class MotorSimulacion:
    def __init__(self):
        # --- ESTADO DE PLANTA Y ESD ---
        self.esd_activo = False
        
        # --- MÓDULO 3: SEPARADOR V-01 ---
        self.presion = 115.0     # psi (Variable base)
        self.presion_v01 = 45.0 # psi (V-01)
        self.nivel = 14.2        # %
        self.nivel_v01 = 60.0    # % (V-01)
        self.caudal_base = 450.0 # BPD base pozo
        self.caudal_entrada = 3000.0 # BPD total planta
        
        # --- MÓDULO 4 Y 5: TEMPERATURA, BSW Y RVP (RES. 35/2021) ---
        self.temp_horno = 62.4   # °C
        self.bsw = 0.5           # %
        self.rvp = 65.0          # kPa

        # --- MÓDULO 2 Y 8: AIB Y MANTENIMIENTO ---
        self.spm_aib = 8.0
        self.carrera_aib = 100.0
        self.horas_motor_aib = 4800  # Horas acumuladas
        
        # --- HISTORIAL PARA GRÁFICOS SCADA ---
        self.historial = []

    def actualizar_ciclo(self):
        """Método invocado en background por app.py en cada rerun"""
        if self.esd_activo:
            self.caudal_base = 0.0
            self.caudal_entrada = 0.0
            self.presion = min(self.presion + 0.1, 160.0)
            return

        # 1. Fluctuaciones dinámicas normales
        self.presion += random.uniform(-0.5, 0.5)
        self.caudal_base += random.uniform(-1.0, 1.0)
        
        # 2. Lógica no lineal del BSW según la Temperatura del Horno
        if self.temp_horno < 40.0:
            self.bsw = 5.5  # Fuera de norma (BSW > 1%)
        else:
            self.bsw = max(0.2, round(1.5 - (self.temp_horno / 60.0), 2))

        # 3. Lógica de RVP (Volatilidad / Res. 35/2021)
        self.rvp = max(45.0, round(95.0 - (self.temp_horno * 0.5), 1))

    def obtener_datos(self):
        """Compatibilidad con app.py y modulo_produccion_recorredor"""
        self.actualizar_ciclo()
        return {
            "presion": round(self.presion, 2),
            "nivel": round(self.nivel, 2),
            "caudal": round(self.caudal_base, 2)
        }

    def obtain_datos(self):
        """Alias de compatibilidad para evitar AttributeError"""
        return self.obtener_datos()

    def activar_esd(self):
        """Cierra las SDV (Válvulas de Seguridad)"""
        self.esd_activo = True
        self.caudal_base = 0.0
        self.caudal_entrada = 0.0

    def reset_planta(self):
        """Normaliza la planta después de un ESD o mantenimiento"""
        self.esd_activo = False
        self.presion = 115.0
        self.presion_v01 = 45.0
        self.nivel = 14.2
        self.nivel_v01 = 60.0
        self.caudal_base = 450.0
        self.caudal_entrada = 3000.0
        self.horas_motor_aib = 0

    def evolucion_produccion(self):
        """Genera el array de datos que requiere el gráfico de scada.py"""
        if not self.historial:
            self.historial = np.random.normal(self.caudal_base, 15, 24).tolist()
        else:
            nuevo_dato = self.caudal_base + random.uniform(-5, 5)
            self.historial.append(nuevo_dato)
            if len(self.historial) > 24:
                self.historial.pop(0)
                
        return self.historial

    def simular_golpe_de_gas(self):
        """Simulación de evento inestable en separador"""
        self.presion += 20.0
        self.nivel = max(0.0, self.nivel - 2.0)
