import random
import time
import numpy as np

class MotorSimulacion:
    def __init__(self):
        # --- ESTADOS GENERALES Y ESD ---
        self.esd_activo = False
        self.inicio_tiempo = time.time()
        
        # --- MÓDULO SCADA Y SEPARADOR V-01 ---
        self.presion = 115.0              # psi base pozo
        self.presion_v01 = 45.0          # psi (Slider V-01)
        self.p_manifold = 145.0          # psi base manifold
        self.nivel = 14.2                # %
        self.nivel_v01 = 60.0            # %
        self.caudal_base = 450.0         # BPD pozo
        self.caudal_entrada = 3000.0     # BPD total
        
        # --- HORNO Y SEGURIDAD ---
        self.temp_horno = 62.4           # °C (TSH-202)
        self.permiso_trabajo_caliente = False  # Checkbox Supervisor
        
        # --- TRATAMIENTO QUÍMICO ---
        self.revision_quimica = False    # Checkbox Supervisor
        self.tiempo_sin_quimica = 0.0
        self.bsw = 0.5                   # % base
        self.rvp = 65.0                  # kPa
        
        # --- MANTENIMIENTO AIB (MENFA-001) ---
        self.spm_aib = 8.0
        self.carrera_aib = 100.0
        self.horas_motor_aib = 4820.0    # Acumulado dinámico
        self.ultimo_tick = time.time()
        self.reparando_aib = False
        self.falla_mecanica_aib = False
        
        # --- SISTEMA DE ALARMAS SCADA ---
        self.alarmas = {
            "TSH-202": {"tag": "Horno T-202", "estado": "NORMAL", "descripcion": "Alta Temp. Horno (>85°C)"},
            "PSH-101": {"tag": "Manifold P-101", "estado": "NORMAL", "descripcion": "Alta Presión Manifold (>180 psi)"},
            "LSHH-01": {"tag": "Separador V-01", "estado": "NORMAL", "descripcion": "Nivel Crítico Separador (>90%)"}
        }
        
        self.historial = []

    def verificar_atributos_guardacostas(self):
        """Parche de memoria viva para evitar AttributeError en Streamlit"""
        if not hasattr(self, 'p_manifold'):
            self.p_manifold = 145.0
        if not hasattr(self, 'presion_v01'):
            self.presion_v01 = 45.0
        if not hasattr(self, 'nivel_v01'):
            self.nivel_v01 = 60.0
        if not hasattr(self, 'revision_quimica'):
            self.revision_quimica = False
        if not hasattr(self, 'permiso_trabajo_caliente'):
            self.permiso_trabajo_caliente = False
        if not hasattr(self, 'horas_motor_aib'):
            self.horas_motor_aib = 4820.0
        if not hasattr(self, 'reparando_aib'):
            self.reparando_aib = False
        if not hasattr(self, 'falla_mecanica_aib'):
            self.falla_mecanica_aib = False
        if not hasattr(self, 'alarmas'):
            self.alarmas = {
                "TSH-202": {"tag": "Horno T-202", "estado": "NORMAL", "descripcion": "Alta Temp. Horno (>85°C)"},
                "PSH-101": {"tag": "Manifold P-101", "estado": "NORMAL", "descripcion": "Alta Presión Manifold (>180 psi)"},
                "LSHH-01": {"tag": "Separador V-01", "estado": "NORMAL", "descripcion": "Nivel Crítico Separador (>90%)"}
            }

    def actualizar_ciclo(self):
        self.verificar_atributos_guardacostas()
        ahora = time.time()
        dt = ahora - self.ultimo_tick
        self.ultimo_tick = ahora

        if self.esd_activo:
            self.caudal_base = 0.0
            self.caudal_entrada = 0.0
            self.presion = min(self.presion + 0.1, 160.0)
            return

        # 1. CÁLCULO DINÁMICO DE PRESIÓN: P-Manifold vinculada a P-Separador V-01
        delta_p_v01 = self.presion_v01 - 45.0
        self.p_manifold = round(145.0 + (delta_p_v01 * 1.2) + random.uniform(-0.3, 0.3), 2)
        self.presion = round(115.0 + random.uniform(-0.5, 0.5), 2)

        # 2. TRIGGER DE INYECCIÓN QUÍMICA (Penalización por Checkbox desactivado)
        if not self.revision_quimica:
            self.tiempo_sin_quimica += dt
            if self.tiempo_sin_quimica >= 120:  # Pasados 2 minutos
                self.bsw = 5.5  # Penalización fija
        else:
            self.tiempo_sin_quimica = 0.0
            self.bsw = max(0.2, round(1.5 - (self.temp_horno / 60.0), 2))

        # Cálculo de RVP (Res. 35/2021)
        self.rvp = max(45.0, round(95.0 - (self.temp_horno * 0.5), 1))

        # 3. CONTADOR DINÁMICO DE HORAS DE MARCHA (AIB)
        if not self.reparando_aib and not self.falla_mecanica_aib:
            self.horas_motor_aib += dt * 0.01  # 1s real = 0.01h simulación

            if self.horas_motor_aib > 4850.0 and self.spm_aib > 10.0:
                self.falla_mecanica_aib = True
                self.spm_aib = 0.0
                self.caudal_base = 0.0

        # 4. TRIGGERS Y LÓGICA DE ALARMAS SCADA
        # Alarm TSH-202 (Horno)
        if self.temp_horno > 85.0:
            if self.alarmas["TSH-202"]["estado"] == "NORMAL":
                self.alarmas["TSH-202"]["estado"] = "ACTIVA"
        else:
            if self.alarmas["TSH-202"]["estado"] in ["ACTIVA", "ACK"]:
                self.alarmas["TSH-202"]["estado"] = "CLEAR"

        # Alarm PSH-101 (Manifold)
        if self.p_manifold > 180.0:
            if self.alarmas["PSH-101"]["estado"] == "NORMAL":
                self.alarmas["PSH-101"]["estado"] = "ACTIVA"
        else:
            if self.alarmas["PSH-101"]["estado"] in ["ACTIVA", "ACK"]:
                self.alarmas["PSH-101"]["estado"] = "CLEAR"

        # Alarm LSHH-01 (Nivel Separador)
        if self.nivel_v01 > 90.0:
            if self.alarmas["LSHH-01"]["estado"] == "NORMAL":
                self.alarmas["LSHH-01"]["estado"] = "ACTIVA"
        else:
            if self.alarmas["LSHH-01"]["estado"] in ["ACTIVA", "ACK"]:
                self.alarmas["LSHH-01"]["estado"] = "CLEAR"

    def reconocer_alarma(self, tag):
        """Pasa la alarma de ACTIVA a ACK (Reconocida)"""
        if tag in self.alarmas and self.alarmas[tag]["estado"] == "ACTIVA":
            self.alarmas[tag]["estado"] = "ACK"

    # --- MÉTODOS DE COMPATIBILIDAD Y MANIOBRAS ---
    def obtener_datos(self):
        self.actualizar_ciclo()
        return {
            "presion": round(self.presion, 2),
            "nivel": round(self.nivel, 2),
            "caudal": round(self.caudal_base, 2)
        }

    def obtain_datos(self):
        return self.obtener_datos()

    def activar_esd(self):
        self.esd_activo = True
        self.caudal_base = 0.0
        self.caudal_entrada = 0.0

    def reset_planta(self):
        self.esd_activo = False
        self.presion = 115.0
        self.presion_v01 = 45.0
        self.p_manifold = 145.0
        self.nivel = 14.2
        self.nivel_v01 = 60.0
        self.caudal_base = 450.0
        self.caudal_entrada = 3000.0
        self.horas_motor_aib = 0.0
        self.falla_mecanica_aib = False
        self.reparando_aib = False

    def evolucion_produccion(self):
        if not self.historial:
            self.historial = np.random.normal(self.caudal_base, 15, 24).tolist()
        else:
            nuevo_dato = self.caudal_base + random.uniform(-5, 5)
            self.historial.append(nuevo_dato)
            if len(self.historial) > 24:
                self.historial.pop(0)
        return self.historial

    def simular_golpe_de_gas(self):
        self.presion += 20.0
        self.presion_v01 += 25.0
        self.nivel = max(0.0, self.nivel - 2.0)
