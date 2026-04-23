import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def show():
    st.header("📈 Análisis de Nodo: IPR vs VLP")
    st.write("Instructor: Fabricio Pizzolato - Optimización de Producción")

    # Recuperamos el factor de falla del simulador de fallas
    factor = st.session_state.get('factor_obstruccion', 1.0)

    with st.sidebar.expander("🛠️ Parámetros del Reservorio", expanded=True):
        p_res = st.number_input("Presión de Reservorio (Pr) [psi]", value=3000)
        pi = st.number_input("Índice de Productividad (IP)", value=1.5)
        
    # --- CÁLCULO DE IPR ---
    caudal_max = pi * p_res
    caudales = np.linspace(0, caudal_max, 50)
    pwf = p_res - (caudales / pi)
    pwf = np.maximum(pwf, 0)

    # --- CÁLCULO DE VLP (Con impacto de falla) ---
    # El factor multiplica la resistencia al flujo (exponente de turbulencia)
    vlp = 500 + (0.05 * factor * caudales**1.8) 

    # --- GRÁFICO INTERACTIVO ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=caudales, y=pwf, name="IPR (Oferta)",
                             line=dict(color='royalblue', width=4)))
    
    fig.add_trace(go.Scatter(x=caudales, y=vlp, name="VLP (Demanda)",
                             line=dict(color='firebrick', width=4, dash='dash')))

    fig.update_layout(
        title=f"Curvas de Inflow y Outflow (Estado: {'Falla' if factor > 1 else 'Normal'})",
        xaxis_title="Caudal de Líquido (STB/D)",
        yaxis_title="Presión de Fondo Fluyente (Pwf) [psi]",
        template="plotly_dark",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- ACCIONES DE REMEDIACIÓN ---
    st.subheader("📋 Diagnóstico y Acción")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if factor > 1.0:
            st.error(f"⚠️ Alerta: Restricción detectada (Factor: {factor})")
            if st.button("💉 Inyectar Solvente / Hot Oil"):
                st.session_state.factor_obstruccion = 1.0
                st.success("Tratamiento aplicado. Limpiando líneas...")
                st.rerun()
        else:
            st.success("✅ Flujo sin restricciones significativas.")
            st.metric("Punto de Operación", "Óptimo")

    with col2:
        st.info("""
        **Interpretación para el examen:**
        1. Si la curva roja (VLP) sube, el pozo produce menos por causas mecánicas.
        2. Si la intersección ocurre a presiones muy altas, el sistema está sufriendo.
        """)
