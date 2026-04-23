import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

# --- CONEXIÓN DE RUTAS (Fuerza bruta para Streamlit Cloud) ---
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)

# Intentamos importar el motor con manejo de error específico
try:
    from motor.motor_simulacion import MotorSimulacion
except Exception as e:
    st.error(f"❌ Error crítico de conexión con el motor: {e}")
    # Definimos una clase temporal para que la app no explote mientras arreglás la carpeta
    class MotorSimulacion:
        def evolucion_produccion(self): return [0] * 10

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
