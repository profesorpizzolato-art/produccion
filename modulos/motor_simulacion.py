import random
import time
import numpy as np

class MotorSimulacion:
    def __init__(self):
        # --- ESTADOS GENERALES Y ESD ---
        self.esd_activo = False
        self.inicio_tiempo = time.time()
        
        # --- MÓDULO SCADA Y SEPARADOR V-01 ---
        self.presion_v01 = 45.0          # psi (Slider V-01)
        self.p_manifold = 145.0          # psi base manifold
        self.nivel_v01 = 60.0            # %
        self.caudal_base = 450.0         # BPD
        
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

    def actualizar_ciclo(self):
        ahora = time.time()
        dt = ahora - self.ultimo_tick
        self.ultimo_tick = ahora

        if self.esd_activo:
            self.caudal_base = 0.0
            return

        # 1. CÁLCULO DINÁMICO DE PRESIÓN: P-Manifold vinculada a P-Separador V-01
        # Presión Base Manifold (145.0 psi) + Impacto directo de presurización del V-01
        delta_p_v01 = self.presion_v01 - 45.0
        self.p_manifold = round(145.0 + (delta_p_v01 * 1.2) + random.uniform(-0.3, 0.3), 2)

        # 2. TRIGGER DE INYECCIÓN QUÍMICA (Penalización por Checkbox desactivado)
        if not self.revision_quimica:
            self.tiempo_sin_quimica += dt
            if self.tiempo_sin_quimica >= 120:  # Pasados 2 minutos (120 s)
                self.bsw = 5.5  # Penalización fija del 5.5%
        else:
            self.tiempo_sin_quimica = 0.0
            # Recupera BSW óptimo según temperatura del horno
            self.bsw = max(0.2, round(1.5 - (self.temp_horno / 60.0), 2))

        # 3. CONTADOR DINÁMICO DE HORAS DE MARCHA (AIB)
        if not self.reparando_aib and not self.falla_mecanica_aib:
            # Incremento proporcional (1 seg real = 0.01 hs simulación)
            self.horas_motor_aib += dt * 0.01

            # TRIGGER DE FALLA DEL MOTOR (MENFA-001)
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

    def reconocer_alarma(self, tag):
        """Pasa la alarma de ACTIVA a ACK (Reconocida)"""
        if tag in self.alarmas and self.alarmas[tag]["estado"] == "ACTIVA":
            self.alarmas[tag]["estado"] = "ACK"
