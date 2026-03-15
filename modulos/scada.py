import streamlit as st
import matplotlib.pyplot as plt
from motor.motor_simulacion import MotorSimulacion

def scada():

    st.header("SCADA Producción")

    motor = MotorSimulacion()

    datos = motor.evolucion_produccion()

    fig, ax = plt.subplots()

    ax.plot(datos)

    ax.set_title("Producción del Campo")

    st.pyplot(fig)
