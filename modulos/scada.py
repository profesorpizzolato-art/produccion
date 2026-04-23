import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

# Aseguramos que Python encuentre la carpeta 'motor' subiendo un nivel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from motor.motor_simulacion import MotorSimulacion
except ModuleNotFoundError:
    st.error("No se pudo encontrar el módulo 'motor'. Verifique la estructura de carpetas.")

def show(): # Cambiado de 'scada' a 'show' para coincidir con app.py
    st.header("🖥️ SCADA de Producción - Planta MENFA")
    st.write("Instructor: Fabricio Pizzolato")

    # Inicializamos el motor
    try:
        motor = MotorSimulacion()
        
        # Simulamos la obtención de datos históricos o evolución
        # Asegúrate de que esta función exista en tu clase MotorSimulacion
        datos = motor.evolucion_produccion() 

        # --- GENERACIÓN DEL GRÁFICO ---
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(datos, color='#00ff00', linewidth=2, label="Caudal STB/D")
        
        # Estética industrial (Fondo oscuro)
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        ax.grid(True, linestyle='--', alpha=0.3)
        
        ax.set_title("Evolución de Producción del Campo", color='white', fontsize=14)
        ax.set_xlabel("Tiempo (intervalos)", color='white')
        ax.set_ylabel("Caudal (bbl)", color='white')
        ax.legend()

        st.pyplot(fig)

        # --- PANEL DE VALORES INSTANTÁNEOS ---
        col1, col2, col3 = st.columns(3)
        actual = datos[-1] if len(datos) > 0 else 0
        col1.metric("Caudal Actual", f"{actual:.2f} bbl/d", delta="Estable")
        col2.metric("Presión de Línea", "145 psi", delta="-2 psi")
        col3.metric("Nivel Tanque 1", "13.8 ft", delta="0.1 ft")

    except Exception as e:
        st.error(f"Error en el Motor de Simulación: {e}")
        st.info("💡 Consejo: Verificá que 'evolucion_produccion()' devuelva una lista o array en motor_simulacion.py")
