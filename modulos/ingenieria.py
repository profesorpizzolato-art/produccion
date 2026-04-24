import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def mostrar_ingenieria():
    st.header("📈 Análisis Nodal: Curvas IPR vs VLP")
    st.write("Optimización del punto de operación del pozo.")

    # --- 1. ENTRADA DE DATOS TÉCNICOS ---
    with st.sidebar:
        st.subheader("⚙️ Parámetros del Reservorio")
        pr = st.slider("Presión de Reservorio (Pr) [psi]", 1000, 4000, 2500)
        ip = st.slider("Índice de Productividad (IP)", 0.5, 5.0, 1.5)
        
        st.subheader("🏗️ Parámetros de Instalación")
        p_cabeza = st.slider("Presión de Cabeza (Pwh) [psi]", 50, 500, 150)

    # --- 2. CÁLCULO DE CURVAS ---
    # Curva IPR (Straight Line - Simplificada)
    q_max = pr * ip
    caudal_ipr = np.linspace(0, q_max, 50)
    presion_ipr = pr - (caudal_ipr / ip)

    # Curva VLP (Simplificada para simulación)
    caudal_vlp = np.linspace(10, q_max, 50)
    # Ecuación cuadrática simple para representar pérdidas por fricción y peso de columna
    presion_vlp = p_cabeza + (0.0005 * caudal_vlp**2) + (0.2 * caudal_vlp)

    # --- 3. GRÁFICO INTERACTIVO ---
    fig = go.Figure()

    # Añadir IPR
    fig.add_trace(go.Scatter(x=caudal_ipr, y=presion_ipr, name='IPR (Yacimiento)',
                             line=dict(color='#2ecc71', width=4)))
    
    # Añadir VLP
    fig.add_trace(go.Scatter(x=caudal_vlp, y=presion_vlp, name='VLP (Instalación)',
                             line=dict(color='#e74c3c', width=4)))

    fig.update_layout(
        title="Punto de Operación (Intersección IPR-VLP)",
        xaxis_title="Caudal (Q) [bpd]",
        yaxis_title="Presión de Fondo (Pwf) [psi]",
        template="plotly_dark",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- 4. ANÁLISIS DE RESULTADOS ---
    # Encontrar intersección aproximada
    idx = np.argwhere(np.diff(np.sign(presion_ipr - presion_vlp))).flatten()
    
    if len(idx) > 0:
        q_op = round(caudal_ipr[idx[0]], 2)
        pwf_op = round(presion_ipr[idx[0]], 2)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Caudal de Operación", f"{q_op} bpd")
        c2.metric("Pwf de Operación", f"{pwf_op} psi")
        c3.metric("Potencial Máximo (AOF)", f"{round(q_max, 1)} bpd")
        
        st.success(f"💡 El pozo está fluyendo a un régimen estable de {q_op} bpd.")
    else:
        st.error("🚨 Las curvas no se cruzan: El pozo no tiene suficiente energía para fluir con la configuración actual.")

    with st.expander("📝 Nota Técnica para el Alumno"):
        st.write("""
        * **IPR (Inflow Performance Relationship):** Representa la capacidad del reservorio de entregar fluido al pozo.
        * **VLP (Vertical Lift Performance):** Representa el requerimiento de presión para elevar el fluido hasta la superficie.
        * **Optimización:** Variando la Presión de Cabeza o el Diámetro de Tubing (VLP), podemos desplazar el punto de operación.
        """)
