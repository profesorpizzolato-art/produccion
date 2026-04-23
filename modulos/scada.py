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

    try:
        motor = MotorSimulacion()
        # Verificá que en motor_simulacion.py la función se llame EXACTAMENTE así:
        datos = motor.evolucion_produccion() 

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(datos, color='#00ff00', linewidth=2)
        ax.set_title("Producción Real Time", color='white')
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#0e1117')
        
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error de ejecución: {e}")
def show():
    st.header("🖥️ SCADA de Producción - Planta MENFA")
    
    # Inicializamos el estado del ESD en la sesión si no existe
    if 'esd_status' not in st.session_state:
        st.session_state.es_status = False

    motor = MotorSimulacion()
    
    # Sincronizamos el motor con el estado de la sesión
    if st.session_state.get('esd_status'):
        motor.activar_esd()

    # --- BOTÓN DE EMERGENCIA ---
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        if st.button("🚨 ACTIVAR ESD (EMERGENCY SHUT DOWN)", use_container_width=True, type="primary"):
            st.session_state.esd_status = True
            st.rerun()
            
    with col_btn2:
        if st.button("✅ RESETEAR PLANTA (START-UP)", use_container_width=True):
            st.session_state.esd_status = False
            st.rerun()

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
