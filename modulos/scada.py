import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

# --- CONEXIÓN DE EMERGENCIA ---
# Obtenemos la ruta absoluta de la carpeta raíz (donde está app.py)
current_dir = os.path.dirname(os.path.abspath(__file__)) # carpeta modulos
root_dir = os.path.dirname(current_dir) # carpeta raiz del proyecto

if root_dir not in sys.path:
    sys.path.append(root_dir)

# Ahora intentamos la importación con la ruta verificada
try:
    from motor.motor_simulacion import MotorSimulacion
except Exception as e:
    st.error(f"❌ Error de conexión: {e}")
    st.info(f"Ruta actual detectada: {root_dir}")
    # Clase de respaldo para que la interfaz no se rompa
    class MotorSimulacion:
        def evolucion_produccion(self): return [0, 0, 0, 0]
def show():
    st.header("🖥️ SCADA de Producción - Planta MENFA")
    st.write("Instructor: Fabricio Pizzolato")

    # Inicializamos estados si no existen
    if 'esd_status' not in st.session_state: st.session_state.esd_status = False
    if 'reporte_completado' not in st.session_state: st.session_state.reporte_completado = False

    # --- LÓGICA DE CONTROL ---
    if st.session_state.esd_status:
        st.error("🛑 PLANTA BLOQUEADA POR SISTEMA DE EMERGENCIA (ESD)")
        
        # Formulario de Reporte de Incidente
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
                st.session_state.reporte_completado = False # Reseteamos el reporte
                st.rerun()
        else:
            st.button("🚨 ESD ACTIVADO", use_container_width=True, disabled=True)

    with col2:
        # El botón de Reset solo se habilita si el reporte está listo
        if st.session_state.esd_status and st.session_state.reporte_completado:
            if st.button("✅ REARMAR PLANTA (START-UP)", use_container_width=True):
                st.session_state.esd_status = False
                st.session_state.reporte_completado = False
                st.balloons()
                st.rerun()
        else:
            st.button("✅ START-UP BLOQUEADO", use_container_width=True, disabled=True)

    # --- VISUALIZACIÓN DEL SCADA ---
    # (Aquí sigue tu código de gráfico y motor de la respuesta anterior)

    # --- GRÁFICO ---
    datos = motor.evolucion_produccion()
    if st.session_state.get('esd_status'):
        # Si hay ESD, forzamos que el último dato sea 0 en el gráfico
        datos[-1] = 0.0
        st.error("⚠️ SISTEMA EN PARADA DE EMERGENCIA - VÁLVULAS SDV CERRADAS")

    fig, ax = plt.subplots(figsize=(10, 3))
    color_linea = '#ff0000' if st.session_state.get('esd_status') else '#00ff00'
    ax.plot(datos, color=color_linea, linewidth=3)
    ax.set_facecolor('#1e1e1e')
    st.pyplot(fig)
