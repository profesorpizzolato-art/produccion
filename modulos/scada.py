import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

# --- CONEXIÓN DE EMERGENCIA ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 
root_dir = os.path.dirname(current_dir) 

if root_dir not in sys.path:
    sys.path.append(root_dir)

# Intento de importación del motor real
try:
    from motor.motor_simulacion import MotorSimulacion
except Exception as e:
    # Clase de respaldo técnica (Fallback)
    class MotorSimulacion:
        def evolucion_produccion(self): 
            import numpy as np
            return np.random.normal(450, 15, 24).tolist()
        def obtener_datos(self):
            return {"presion": 115.0, "nivel": 14.2, "caudal": 450.0}

def show():
    st.header("🖥️ SCADA de Producción - Planta MENFA")
    st.write("Instructor: Fabricio Pizzolato")

    # Instanciamos el motor dentro de la función para que sea accesible
    motor = MotorSimulacion()

    # Inicializamos estados si no existen
    if 'esd_status' not in st.session_state: st.session_state.esd_status = False
    if 'reporte_completado' not in st.session_state: st.session_state.reporte_completado = False

    # --- LÓGICA DE CONTROL DE EMERGENCIA ---
    if st.session_state.esd_status:
        st.error("🛑 PLANTA BLOQUEADA POR SISTEMA DE EMERGENCIA (ESD)")
        
        with st.expander("📋 REPORTE DE INCIDENTE OBLIGATORIO", expanded=not st.session_state.reporte_completado):
            st.warning("Debe completar el informe técnico para habilitar el Start-Up.")
            causa = st.selectbox("Causa de la Parada:", [
                "Falla Instrumental", "Sobrepresión en Separador", 
                "Fuga de Hidrocarburo", "Falla de Energía", "Prueba de Seguridad"
            ])
            descripcion = st.text_area("Descripción detallada de la maniobra:")
            operador = st.text_input("Firma del Operador:", value="Alumno IPCL")
            
            if st.button("Enviar Reporte y Validar"):
                if len(descripcion) > 10:
                    st.session_state.reporte_completado = True
                    st.success("✅ Reporte archivado. Sistema de seguridad desbloqueado.")
                    st.rerun()
                else:
                    st.error("Por favor, sea más específico en la descripción técnica.")

    # --- BOTONERA DINÁMICA ---
    col1, col2 = st.columns(2)
    with col1:
        if not st.session_state.esd_status:
            if st.button("🚨 ACTIVAR ESD", use_container_width=True, type="primary"):
                st.session_state.esd_status = True
                st.session_state.reporte_completado = False 
                st.rerun()
        else:
            st.button("🚨 ESD ACTIVADO", use_container_width=True, disabled=True)

    with col2:
        if st.session_state.esd_status and st.session_state.reporte_completado:
            if st.button("✅ REARMAR PLANTA (START-UP)", use_container_width=True):
                st.session_state.esd_status = False
                st.session_state.reporte_completado = False
                st.balloons()
                st.rerun()
        else:
            st.button("✅ START-UP BLOQUEADO", use_container_width=True, disabled=True)

    # --- VISUALIZACIÓN DE DATOS ---
    st.divider()
    datos = motor.evolucion_produccion()
    
    # Si hay ESD, simulamos la caída de producción en el gráfico
    if st.session_state.esd_status:
        datos = [d * 0.1 for d in datos[:-1]] + [0.0] # Caída drástica
        st.error("⚠️ FLUJO INTERRUMPIDO - VÁLVULAS DE SEGURIDAD (SDV) CERRADAS")

    # Configuración estética del gráfico SCADA
    fig, ax = plt.subplots(figsize=(10, 3))
    color_linea = '#ff4b4b' if st.session_state.esd_status else '#00ff00'
    
    ax.plot(datos, color=color_linea, linewidth=3, label="Caudal (bbl/d)")
    ax.fill_between(range(len(datos)), datos, color=color_linea, alpha=0.1)
    
    # Estilo Dark Industrial
    ax.set_facecolor('#1e1e1e')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.grid(True, linestyle='--', alpha=0.2)
    ax.set_title("HISTÓRICO DE PRODUCCIÓN (24 HRS)", color='white', loc='left')
    
    st.pyplot(fig)

    # Métricas inferiores
    m1, m2, m3 = st.columns(3)
    val_presion = 165.0 if st.session_state.esd_status else 115.0
    m1.metric("P. Separador", f"{val_presion} psi", delta="ALTA" if st.session_state.esd_status else "Normal")
    m2.metric("Caudal Actual", f"{int(datos[-1])} bpd")
    m3.metric("Estado SDV", "CERRADA" if st.session_state.esd_status else "ABIERTA")
