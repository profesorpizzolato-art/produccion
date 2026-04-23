import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def show():
    st.header("📈 Análisis de Nodo: IPR vs VLP")
    st.write("Instructor: Fabricio Pizzolato - Optimización de Producción")

    with st.sidebar.expander("🛠️ Parámetros del Reservorio", expanded=True):
        p_res = st.number_input("Presión de Reservorio (Pr) [psi]", value=3000)
        pi = st.number_input("Índice de Productividad (IP)", value=1.5)
        pb = st.number_input("Presión de Burbuja (Pb) [psi]", value=1500)

    # --- CÁLCULO DE IPR (Vogel / Darcy) ---
    caudal_max = pi * p_res # Estimación lineal simple
    caudales = np.linspace(0, caudal_max, 50)
    
    # Modelo Simplificado de IPR
    pwf = p_res - (caudales / pi)
    pwf = np.maximum(pwf, 0) # No presiones negativas

    # --- CÁLCULO DE VLP (Curva de Levantamiento) ---
    # Simulamos una restricción de tubería (Tubing)
    vlp = 500 + (0.05 * caudales**1.8) 

    # --- GRÁFICO INTERACTIVO ---
    fig = go.Figure()

    # Curva IPR
    fig.add_trace(go.Scatter(x=caudales, y=pwf, name="IPR (Oferta)",
                             line=dict(color='royalblue', width=4)))
    
    # Curva VLP
    fig.add_trace(go.Scatter(x=caudales, y=vlp, name="VLP (Demanda)",
                             line=dict(color='firebrick', width=4, dash='dash')))

    fig.update_layout(
        title="Curvas de Inflow y Outflow",
        xaxis_title="Caudal de Líquido (STB/D)",
        yaxis_title="Presión de Fondo Fluyente (Pwf) [psi]",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- ANÁLISIS TÉCNICO ---
    st.subheader("📋 Diagnóstico de Producción")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Puntos de Intersección", "Operando", delta="Estable")
        st.write("La intersección de ambas curvas representa el **Punto de Operación** actual del pozo.")
    
    with col2:
        st.info("""
        **Tips para el Alumno:**
        * Si la **IPR** baja, el reservorio pierde energía.
        * Si la **VLP** sube, hay una obstrucción o aumento de contrapresión.
        """)
