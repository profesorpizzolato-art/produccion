import streamlit as st
import numpy as np
import plotly.graph_objects as go

def mostrar_ingenieria():
    st.header("📈 Análisis de Nodal System (IPR vs VLP)")
    st.write("Determinación del punto de operación óptimo del pozo.")

    # --- SIDEBAR DE PARÁMETROS TÉCNICOS ---
    st.sidebar.subheader("Datos del Reservorio (IPR)")
    presion_res = st.sidebar.slider("Presión Reservorio (psi)", 1000, 5000, 3000)
    ip = st.sidebar.slider("Índice Productividad (bpd/psi)", 0.5, 5.0, 1.5)
    
    st.sidebar.subheader("Datos de Instalación (VLP)")
    p_cabezal = st.sidebar.slider("Presión Cabezal (psi)", 100, 800, 250)
    friccion = st.sidebar.slider("Factor de Fricción", 0.01, 0.1, 0.03)

    # --- CÁLCULOS LÓGICOS ---
    # Curva IPR (Ecuación lineal simple para este ejemplo)
    caudal_max = ip * presion_res
    q_ipr = np.linspace(0, caudal_max, 50)
    pwf_ipr = presion_res - (q_ipr / ip)

    # Curva VLP (Modelo simplificado de demanda de presión)
    q_vlp = np.linspace(10, caudal_max, 50)
    # Pwf = Pcabezal + Hidrostática + Fricción (simplificado)
    pwf_vlp = p_cabezal + 1500 + (friccion * (q_vlp**1.8))

    # --- GRÁFICO INTERACTIVO ---
    fig = go.Figure()

    # Añadir IPR
    fig.add_trace(go.Scatter(x=q_ipr, y=pwf_ipr, name='Oferta (IPR)', line=dict(color='green', width=3)))
    
    # Añadir VLP
    fig.add_trace(go.Scatter(x=q_vlp, y=pwf_vlp, name='Demanda (VLP)', line=dict(color='red', width=3)))

    fig.update_layout(
        title="Curvas de Performance del Pozo",
        xaxis_title="Caudal de Líquido (BPD)",
        yaxis_title="Presión de Fondo Fluyente (psi)",
        template="plotly_dark",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- ANÁLISIS DE RESULTADOS ---
    st.success("💡 **Interpretación:** El punto donde las curvas se cruzan es el caudal real de producción bajo las condiciones actuales.")
