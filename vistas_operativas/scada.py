import streamlit as st
import time

def render_scada():
    st.title("🖥️ Sistema SCADA Central")
    motor = st.session_state.motor
    
    # El SCADA avanza un ciclo de simulación para actualizar las físicas de la planta
    datos_actuales = motor.actualizar_ciclo()
    
    # Bloque de Alarmas Integradas (Opción 3: Historia Operacional)
    if datos_actuales["separador"]["alarma_alta"]:
        st.error("🚨 ALARMA: ¡Nivel Alto en Separador Bifásico!")
    
    if datos_actuales["lact"]["rechazo_bsw"]:
        st.warning("⚠️ RECHAZO LACT: BSW fuera de especificación comercial.")
        
    # Desplegar indicadores
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Presión Separador", f"{datos_actuales['separador']['presion']:.2f} psi")
    with col2:
        st.metric("Nivel Separador", f"{datos_actuales['separador']['nivel']:.2f} ft")
        
    # Gráfico de tendencias histórico real
    st.line_chart(datos_actuales["sistema"]["historial_caudal"])
