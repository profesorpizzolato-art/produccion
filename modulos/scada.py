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
