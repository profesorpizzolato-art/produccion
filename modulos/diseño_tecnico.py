import numpy as np

def calcular_especificaciones_bes(q, profundidad, bsw):
    """Calcula parámetros básicos para Bombeo Electrosumergible"""
    # Ejemplo simple: Carga dinámica total (TDH)
    gradiente_fluido = (0.433 * (1 - bsw/100)) + (0.35 * (bsw/100)) # Simplificado
    tdh = profundidad * gradiente_fluido * 1.1 # 10% extra por fricción
    etapas = tdh / 50 # Asumiendo 50ft de cabeza por etapa
    potencia = (q * tdh) / (135770 * 0.65) # HP aproximados
    
    return {
        "tdh": round(tdh, 2),
        "etapas": int(etapas),
        "potencia": round(potencia, 2)
    }

def calcular_especificaciones_bm(q, profundidad):
    """Cálculos para Bombeo Mecánico"""
    # Lógica para SPM y Torque
    spm = (q / 25) # Estimación burda para el ejemplo
    return {
        "spm": round(spm, 1),
        "unidad": "API 320-256-120"
    }
